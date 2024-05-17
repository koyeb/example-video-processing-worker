<div align="center">
  <a href="https://koyeb.com">
    <img src="https://www.koyeb.com/static/images/icons/koyeb.svg" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Koyeb Serverless Platform</h3>
  <p align="center">
    Deploy a video processing pipeline worker service on Koyeb
    <br />
    <a href="https://koyeb.com">Learn more about Koyeb</a>
    ·
    <a href="https://koyeb.com/docs">Explore the documentation</a>
    ·
    <a href="https://koyeb.com/tutorials">Discover our tutorials</a>
  </p>
</div>


## About Koyeb and the video processing pipeline worker service

Koyeb is a developer-friendly serverless platform to deploy apps globally. No-ops, servers, or infrastructure management.  This repository contains a job search application you can deploy on the Koyeb serverless platform for testing.

This example worker, when deployed alongside its companion [video processing web app](https://github.com/koyeb/example-video-processing-app), allows you to upload videos that will be automatically tagged and categorized by AssemblyAI.  This repository is the video processing worker service built with FastAPI.  It processes videos uploaded to the web app by querying the AssemblyAI API.

## Getting Started

Follow the steps below to deploy and run the example video processing pipeline worker service on your Koyeb account.

### Requirements

* A [Koyeb account](https://app.koyeb.com/auth/signup) to build, deploy, and run this application.
* An [AssemblyAI API key](https://www.assemblyai.com/dashboard/signup) to integrate AI-driven video tagging and classification capabilities.  **Note:** You will need to add credit to your account to use the LLM features implemented in this guide.

### Deploy using the Koyeb button

Once the [web application](https://github.com/koyeb/example-video-processing-app) is deployed, you can deploy this service worker.  Navigate to the previous created application in the [Koyeb control panel](https://app.koyeb.com/) and click **Create Service**:

1. Select **GitHub** as your deployment method and select your GitHub project for the worker service API if you forked this project.  Alternatively, enter `https://github.com/koyeb/example-video-processing-worker` in the **Public GitHub repository** field to use this repository as-is.
2. In the **Builder** section, override the **Run command** with `uvicorn main:app --port 8080 --host 0.0.0.0`.
3. In the **Environment variables** section, configure the following environment variable: `ASSEMBLYAI_API_KEY=<YOUR_ASSEMBLYAI_API_KEY>`.
4. In the **Scaling** section, select **Autoscaling** from 1 to 3 Instances. Set the number of requests per second to your desired threshold.
5. In the **Exposed ports** section, deselect the **Public** toggle to make it only accessible from the service mesh and set the port to **8080**.
6. In the **App and Service names** section, set the **Service name** to the value you chose in the `WORKER_URL` variable when you deployed the Django application.
7. Click **Deploy**.

Your web application and service worker should now be up and running. When you upload a video, it will automatically be processed by the worker service with the help of AssemblyAI.

## Contributing

If you have any questions, ideas or suggestions regarding this application sample, feel free to open an [issue](https://github.com/koyeb/example-video-processing-worker/issues) or fork this repository and open a [pull request](https://github.com/koyeb/example-video-processing-worker/pulls).

## Contact

[Koyeb](https://www.koyeb.com) - [@gokoyeb](https://twitter.com/gokoyeb) - [Slack](http://slack.koyeb.com/)
