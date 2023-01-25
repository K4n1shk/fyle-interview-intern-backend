from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources',__name__)

@teacher_assignments_resources.route('/assignments',methods=['GET'],strict_slashes=False)
@decorators.auth_principal
def list_submitted_assignments(p):
    """Return lists of assignments submitted to teacher"""
    submitted_assignmets = Assignment.get_assignments_by_teacher(p.teacher_id)
    submitted_assignmets_dump = AssignmentSchema().dump(submitted_assignmets,many=True)
    return APIResponse.respond(data=submitted_assignmets_dump)

@teacher_assignments_resources.route('/assignments/grade',methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_submitted_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_submitted_assignment_payload = incoming_payload
    graded_assignment = Assignment.grade_assignment(
        _id = grade_submitted_assignment_payload['id'],
        grade = grade_submitted_assignment_payload['grade'],
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

