import uuid

from .models import VisitSession


def get_or_create_visit_session(request):
    visit_session_id = request.session.get("visit_session_id")

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
            return visit_session

    visit_session = VisitSession.objects.create(
        session_key=str(uuid.uuid4())
    )

    request.session["visit_session_id"] = visit_session.id

    return visit_session