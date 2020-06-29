# Cloud Development Kit deployment for Cowrie honeypots!

This is a project build with Python and AWS CDK. The goal is to have SSH honeypot infrastructure deployed and destroyed within seconds and logged to to CloudWatch for persistence or a Splunk instance can ingest it (for example).

The `cdk.json` file tells the CDK Toolkit how to execute this app.
To manually create a virtualenv execute:

```
python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .env/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Deploy it
Run the bootstrap for the stack

```
cdk bootstrap
```

And then deploy it

```
cdk deploy cdk-cowrie-honeypots
```

And you're done!

## Infrastructure overview
![CDK Cowrie infrastructure](https://github.com/nheijmans/cdk_cowrie_honeypots/raw/master/visual/cdk-honeypots-infra-visual.jpg)

## Useful CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy the honeypots and easy deployment!
