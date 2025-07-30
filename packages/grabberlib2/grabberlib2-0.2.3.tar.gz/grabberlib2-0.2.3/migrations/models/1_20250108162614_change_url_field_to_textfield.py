from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "extractedpage" ALTER COLUMN "url" TYPE TEXT USING "url"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "extractedpage" ALTER COLUMN "url" TYPE VARCHAR(255) USING "url"::VARCHAR(255);"""
