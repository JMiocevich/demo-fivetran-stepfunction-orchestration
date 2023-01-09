# Fivetran DBT Stepfunction Orchestration


Initial deployment into your account:
* Configure AWS credentials

#### Requirements
- aws sam (homebrew installation)

```
brew tap aws/tap
brew install aws-sam-cli
```
- [Docker](https://docs.docker.com/desktop/install/mac-install/)

#### Architecture Diagram
<img src="/www/architecture_diagram.png" alt="drawing" width="800"/>


### Sandbox Deployment

1. Change stack_name to desired name in ```./ci/scripts/sandbox-deploy.sh ```
2. Run ```./ci/scripts/sandbox-deploy.sh ``` to deploy stack
3. Update ```FivetranKey``` and  ```FivetranSecret``` Secrets in secret manager. See [Fivetran Docs](https://fivetran.com/docs/rest-api/getting-started) to create API key
4. To create snowflake b64 key, run this command ```openssl base64 -in [filename] | pbcopy``` on your private key and copy into ```SnowflakePrivateKey``` secret
5. Create [new webhook](https://developers.fivetran.com/openapi/reference/v1/operation/create_group_webhook/) on desired fivetran group 
6. Update dbt profile at  ```src/ecs/dbt_project/profiles.yml``` to match your desiredusername and desired database
7. Update src/ecs/dbt_project as needed 
8. Start New StepFunction Excecution with the following json input (insert your fivetran group_id)
   
    ```
    {
        "group_id": "Insert_group_id_here"
    }
    ```
    example:
    ```
    {
        "group_id": "iii_outgrow"
    }
    ```

9.  Run ```sam delete --region ap-southeast-2``` and follow prompts to teardown stack
10.  [Delete fivetran webook](https://developers.fivetran.com/openapi/reference/v1/operation/delete_webhook/)





