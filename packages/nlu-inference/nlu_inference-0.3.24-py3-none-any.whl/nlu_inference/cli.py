from jsonargparse import CLI 
from .io import ParserOutput, HealthCheckOutput, DomainOutput, NLUInput
from .language import NLU
import uvicorn
from .utils import print_spent_time
from wasabi import msg
from .log_utils_fastapi import RequestContextMiddleware,setup_logging,get_logger
from contextvars import copy_context
import asyncio

def serve(checkpoint: str, example: str = '你好', port: int = 18000, host: str = "localhost"):
    
    nlu = NLU.from_checkpoint(checkpoint)
    
    domain = nlu.domain
    
    
    msg.info(f"loading model {domain}")
    
    from fastapi import FastAPI
    app = FastAPI(description=f"{domain} Inference API")
    app.add_middleware(RequestContextMiddleware)
    @app.post("/parser", response_model=ParserOutput)
    async def parse(inputs: NLUInput):
        with print_spent_time("parser"):
            context = copy_context()
            # result = await asyncio.create_task(context.run(inference_batch,texts))
            # output: ParserOutput = nlu.predict_parser(inputs.rawText)
            output: ParserOutput = await asyncio.create_task(context.run(nlu.predict_parser,inputs.rawText))
        return output
    
    
    @app.post("/domain", response_model=DomainOutput)
    def domain(inputs: NLUInput):
        with print_spent_time("domain"):
            output =  nlu.predict_domain(inputs.rawText)
        return output
    
    
    @app.post("/health", response_model=HealthCheckOutput)
    def health():
        try:
            domain_results = nlu.predict_domain(example)
            parser_results = nlu.predict_parser(example)
            return HealthCheckOutput(code=0, message="success")
        except Exception as e:
            return HealthCheckOutput(code=1, message=str(e))
        
    @app.get("/health")
    def health():
        try:
            domain_results = nlu.predict_domain(example)
            parser_results = nlu.predict_parser(example)
            return {"code": 0, "message": "success"}
        except Exception as e:
            return {"code": 1, "message": str(e)}
        
    uvicorn.run(app, host=host, port=port)


def run():
    CLI(serve)