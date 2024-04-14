Comprehensive Setup Procedure
Create Workflow Files:

Create the above 27303_test.yml and 27303_deploy.yml files in the .github/workflows directory of your GitHub repository.
Set Up GitHub Secrets:

Go to your repository's settings on GitHub.
Navigate to "Secrets" and then "Actions".
Click on "New repository secret".
Add DOCKER_USERNAME and DOCKER_PASSWORD with your DockerHub credentials.
Commit and Push:

Add, commit, and push the workflow files to your repository.
Monitor the Actions:

Once pushed, navigate to the "Actions" tab of your repository to see the workflows being executed.
Ensure that tests run and pass, and that the Docker image is successfully built and pushed to DockerHub when changes are made to the main branch.
Document the Process:

As you monitor the workflows, take screenshots of the GitHub Actions dashboard showing successful and failed builds.
Document each part of the process in a report, explaining what happens during each workflow stage, especially detailing what happens when tests fail.
Generate the Report:

Use a document editor to compile your findings, explanations, and screenshots into a comprehensive report.
Ensure that the report is well-formatted and clearly communicates the setup and outcomes of your CI/CD pipeline.