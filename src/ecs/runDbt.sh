echo "# [Lint] AWS CloudFormation Templates"

echo "# [Deploy] SAM services as nested stack for organisation: '${VALUE}'"

python3 ./main.py

ls
cd dbt_project
dbt run --profiles-dir .
