import re
import logging

from sqlalchemy.exc import IntegrityError

from bugcode.server.models import (
    CVE,
    db,
    Reference,
    PolicyViolation,
    OWASP
)
from bugcode.server.utils.database import is_unique_constraint_violation
from bugcode.server.utils.reference import create_reference

logger = logging.getLogger(__name__)


def parse_cve_references_and_policyviolations(vuln, references, policyviolations, cve_list):
    # add_references(vuln, references)
    vuln.refs = create_reference(references, vuln.id)
    add_policy_violations(vuln, policyviolations)

    parsed_cve_list = []
    for cve in cve_list:
        parsed_cve_list += re.findall(CVE.CVE_PATTERN, cve.upper())

    add_cves(vuln, parsed_cve_list)

    return vuln


def get_or_create_owasp(owasp_name: str) -> [None, OWASP]:
    if not owasp_name:
        logger.error("owasp_name not provided.")
        return None
    owasp = OWASP.query.filter(OWASP.name == owasp_name).first()
    if not owasp:
        try:
            owasp = OWASP(name=owasp_name)
            db.session.add(owasp)
            db.session.commit()
        except IntegrityError as ex:
            if not is_unique_constraint_violation(ex):
                logger.error("Could not create owasp %s", owasp_name)
                return None
            logger.debug("OWASP violated unique constraint. Rollback in progress")
            db.session.rollback()
            owasp = OWASP.query.filter(OWASP.name == owasp_name).first()
            if not owasp:
                logger.error("Could not create owasp")
                return None
            logger.debug("OWASP object finally obtained")
    return owasp


def get_or_create_reference(reference_name: str, reference_type: str, workspace_id: int) -> [None, Reference]:
    logger.debug("Trying to create reference %s with type %s fow ws %s",
                 reference_name,
                 reference_type,
                 workspace_id)
    if not reference_name or not workspace_id:
        logger.error("Reference or workspace not provided.")
        return None
    reference_obj = Reference.query.filter(Reference.name == reference_name,
                                           Reference.type == reference_type,
                                           Reference.workspace_id == workspace_id).first()
    if not reference_obj:
        try:
            reference_obj = Reference(name=reference_name, type=reference_type, workspace_id=workspace_id)
            db.session.add(reference_obj)
            db.session.commit()
        except IntegrityError as ex:
            if not is_unique_constraint_violation(ex):
                logger.exception("Could not create reference %s with type %s fow ws %s", reference_name,
                                 reference_type,
                                 workspace_id,
                                 exc_info=ex)
                return None
            logger.debug("Reference violated unique constraint. Rollback in progress")
            db.session.rollback()
            reference_obj = Reference.query.filter(Reference.name == reference_name,
                                                   Reference.type == reference_type,
                                                   Reference.workspace_id == workspace_id).first()
            if not reference_obj:
                logger.error("Could not get reference")
                return None
            logger.debug("Reference object finally obtained")
    return reference_obj


def add_cves(obj, cves):
    for cve_name in cves:
        cve = CVE.query.filter(CVE.name == cve_name).first()
        if not cve:
            try:
                cve = CVE(name=cve_name)
                db.session.add(cve)
                db.session.commit()
            except IntegrityError as ex:
                if not is_unique_constraint_violation(ex):
                    logger.error("Could not create cve %s", cve_name)
                    logger.exception(ex)
                    continue
                logger.debug("CVE violated unique constraint. Rollback in progress")
                db.session.rollback()
                cve = CVE.query.filter_by(name=cve_name).first()
                if not cve:
                    logger.error("Could not get cve")
                    continue
                logger.debug("CVE object finally obtained")
        obj.cve_instances.add(cve)


def add_references(obj, references):
    for reference_dict in references:
        reference_name = reference_dict.get('name')
        reference = Reference.query.filter(Reference.name == reference_name,
                                           Reference.type == 'other',
                                           Reference.workspace_id == obj.workspace_id).first()
        if not reference:
            try:
                reference = Reference(name=reference_name, type='other', workspace_id=obj.workspace_id)
                db.session.add(reference)
                db.session.commit()
            except IntegrityError as ex:
                if not is_unique_constraint_violation(ex):
                    logger.error("Could not create reference %s", reference_name)
                    logger.exception(ex)
                    continue
                logger.debug("Reference violated unique constraint. Rollback in progress")
                db.session.rollback()
                reference = Reference.query.filter(Reference.name == reference_name,
                                                   Reference.type == 'other',
                                                   Reference.workspace_id == obj.workspace_id).first()
                if not reference:
                    logger.error("Could not get reference")
                    continue
                logger.debug("Reference object finally obtained")
        obj.reference_instances.add(reference)


def add_policy_violations(obj, policy_violations):
    for policy_violation_name in policy_violations:
        policy_violation = PolicyViolation.query.filter(PolicyViolation.name == policy_violation_name,
                                                        PolicyViolation.workspace_id == obj.workspace_id).first()
        if not policy_violation:
            try:
                policy_violation = PolicyViolation(name=policy_violation_name, workspace_id=obj.workspace_id)
                db.session.add(policy_violation)
                db.session.commit()
            except IntegrityError as ex:
                if not is_unique_constraint_violation(ex):
                    logger.error("Could not create policy_violation %s", policy_violation_name)
                    logger.exception(ex)
                    continue
                logger.debug("PolicyViolation violated unique constraint. Rollback in progress")
                db.session.rollback()
                policy_violation = PolicyViolation.query.filter_by(name=policy_violation_name,
                                                                   workspace_id=obj.workspace_id).first()
                if not policy_violation:
                    logger.error("Could not get policy_violation")
                    continue
                logger.debug("PolicyViolation object finally obtained")
        obj.policy_violation_instances.add(policy_violation)
