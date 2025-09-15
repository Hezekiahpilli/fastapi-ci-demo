# FastAPI Lambda Demo

This repository contains a minimal [FastAPI](https://fastapi.tiangolo.com/) application configured to run on AWS Lambda with the help of [Mangum](https://github.com/jordaneremieff/mangum). It serves as a lightweight starting point for building serverless APIs while keeping the local development experience familiar.

## Prerequisites

- Python 3.9 or later
- Install dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

## Local Development

Run the application with Uvicorn to exercise the same root endpoint that Lambda will invoke:

```bash
uvicorn app.main:app --reload
```

Then browse to `http://127.0.0.1:8000/` to confirm the `"FastAPI running on Lambda!"` response.

## Packaging for AWS Lambda

1. Use the provided `Dockerfile.lambda` to build your dependency layer and application package:
   ```bash
   docker build -f Dockerfile.lambda -t fastapi-lambda-builder .
   docker run --rm -v "$PWD":/workspace fastapi-lambda-builder
   ```
   The container writes the Lambda-compatible dependencies into either `lambda-package/` or `package/`, depending on your workflow preference.
2. Zip the resulting folder (for example, `lambda-package/`) together with your application code:
   ```bash
   cd lambda-package
   zip -r ../fastapi_lambda.zip .
   ```
3. Upload the generated archive (e.g., `fastapi_lambda.zip`) to your AWS Lambda function via the console, AWS CLI, or your chosen IaC tool.

> **Tip:** If you are deploying with infrastructure-as-code (SAM, CDK, Terraform, etc.), point your deployment configuration to the zipped artifact that contains both the `app/` sources and Mangum-powered dependencies.

## Repository Layout

- `app/` – FastAPI application code, including the Lambda entry point using Mangum.
- `package/` – Optional directory to hold locally built dependencies for manual zipping.
- `lambda-package/` – Docker-generated Lambda package artifacts, ready to zip and upload.
- `requirements.txt` – Python dependencies required by the FastAPI application.
- `fastapi_lambda.zip` – Example deployment artifact produced after packaging (can be regenerated or removed as needed).

Feel free to delete and regenerate any build artifacts (`package/`, `lambda-package/`, or `fastapi_lambda.zip`) as part of your own deployment pipeline.

## Deployment Tips

- Configure Lambda handler to point to `app.main.handler` when creating or updating the function.
- Ensure the function runtime is set to Python 3.9 or a compatible later version.
- For larger dependencies, consider using Lambda Layers or container images built from the same `Dockerfile.lambda` instructions.
- Monitor CloudWatch Logs after deployment to verify the health of the FastAPI application and catch startup issues early.

## Licensing

A dedicated license file is not included in this template. Add your organization's preferred license before distributing your derivative work.

## Contact

Questions or ideas? Open an issue or submit a pull request in this repository so the maintainers can follow up.
