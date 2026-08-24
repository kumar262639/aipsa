import json, logging
logger = logging.getLogger("shopping_assistant.audit")

def audit_tool_call(session_id, tool, success, arguments=None):
    if tool:
        logger.info(json.dumps({"event":"tool_call","session_id":session_id,"tool":tool,
                                "success":success,"arguments":arguments or {}}))
