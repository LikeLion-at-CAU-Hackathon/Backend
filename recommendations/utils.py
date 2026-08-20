import uuid

from .models import VisitSession


def get_or_create_visit_session(request):
    # 1. 프론트에서 명시적으로 보낸 session id 우선 확인
    visit_session_id = (
        request.data.get("visit_session_id")
        if hasattr(request, "data")
        else None
    )

    # 2. body에 없으면 query param도 확인
    if not visit_session_id:
        visit_session_id = request.query_params.get(
            "visit_session_id"
        )

    # 3. 그래도 없으면 Django session cookie 확인
    if not visit_session_id:
        visit_session_id = request.session.get(
            "visit_session_id"
        )

    # 4. 기존 VisitSession이 있으면 재사용
    if visit_session_id:
        visit_session = (
            VisitSession.objects
            .filter(
                id=visit_session_id,
                ended_at__isnull=True,
            )
            .first()
        )

        if visit_session:
            request.session["visit_session_id"] = visit_session.id
            return visit_session

    # 5. 없으면 새 VisitSession 생성
    visit_session = VisitSession.objects.create(
        session_key=str(uuid.uuid4())
    )

    request.session["visit_session_id"] = visit_session.id

    return visit_session