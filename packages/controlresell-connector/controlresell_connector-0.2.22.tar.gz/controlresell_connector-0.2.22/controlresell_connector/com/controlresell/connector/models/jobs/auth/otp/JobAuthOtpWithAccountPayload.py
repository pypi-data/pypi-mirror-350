from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.auth.otp.JobAuthOtpPayload import JobAuthOtpPayload

class JobAuthOtpWithAccountPayload(BaseModel):
    accountId: UUID
    payload: JobAuthOtpPayload
