# pandas_bedrock

This is a simple package to help you get started with [pandas](https://pandas.pydata.org/) and data analysis. It is designed to be used with the [Amazon Bedrock SDK](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html).

## Tested with Foundation Models on Amazon Bedrock

The following Foundation Models have been tested with this package:

| Provider | Model Name | Model ID | 
| --- | --- | --- |
| Anthropic | Claude | anthropic.claude-v2:1 |

## Usage

```python
import pandas
import pandas_bedrock

client = pandas_bedrock.Client(model="anthropic.claude-v2:1", region_name  = "us-east-1", profile_name = "your_aws_profile")

df = pandas.DataFrame({
    'Name': ['Scooby Doo', 'Lassie', 'Snoopy', 'Pluto', 'Santa’s Little Helper'],
    'Breed': ['Great Dane', 'Collie', 'Beagle', 'Mixed', 'Greyhound'],
    'Show': ['Scooby-Doo', 'Lassie', 'Peanuts', 'Disney', 'The Simpsons']
})

client.ask('What show is Snoopy from?', df)
```

## Disclaimers

This package is provided 'as is' and does not carry official support from any recognized entities. While there is no guarantee that it will be compatible with all Foundation Models, your contributions are highly encouraged! For additional information, please consult the Amazon Bedrock SDK documentation. Trademarks, such as company names, product names, and logos, belong to their respective owners.
