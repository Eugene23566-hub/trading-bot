import json
from openai import OpenAI
SCHEMA={"type":"object","properties":{"market_regime":{"type":"string","enum":["risk_on","risk_off","mixed"]},"decisions":{"type":"array","items":{"type":"object","properties":{"symbol":{"type":"string"},"action":{"type":"string","enum":["LONG","SHORT","WAIT"]},"confidence":{"type":"number","minimum":0,"maximum":1},"setup_type":{"type":"string"},"rationale":{"type":"string"},"risk_note":{"type":"string"}},"required":["symbol","action","confidence","setup_type","rationale","risk_note"],"additionalProperties":False}}},"required":["market_regime","decisions"],"additionalProperties":False}
class AIAnalyst:
    def __init__(self,api_key,model): self.client=OpenAI(api_key=api_key); self.model=model
    def analyze(self,market_context,candidates):
        r=self.client.responses.create(model=self.model,reasoning={"effort":"medium"},instructions="You are the decision layer of a crypto paper-trading research system. Never place real trades. Evaluate only supplied data. Prefer WAIT when evidence conflicts. LONG/SHORT requires strong evidence. Do not invent copy-trader data. Confidence >=0.72 should be rare.",input=json.dumps({"market_context":market_context,"candidates":candidates},ensure_ascii=False),text={"format":{"type":"json_schema","name":"crypto_cycle_decisions","schema":SCHEMA,"strict":True}})
        return json.loads(r.output_text)
