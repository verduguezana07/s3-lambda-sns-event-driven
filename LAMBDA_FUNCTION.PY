import json
import boto3
import urllib.parse

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Substitua pelo ARN do seu topico SNS
SNS_TOPIC_ARN = 'arn:aws:sns:us-west-2:581396610808:NotificacaoPalavras'

def lambda_handler(event, context):
    try:
        # Obter informacoes do S3 a partir do evento
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        # Descarregar o conteudo do ficheiro
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Contagem de palavras
        word_count = len(file_content.split())
        
        # Formatacao da mensagem exigida
        message = f"The word count in the {file_key} file is {word_count}."
        subject = "Word Count Result"
        
        # Publicar no SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
    except Exception as e:
        print(f"Erro: {str(e)}")
        raise e
