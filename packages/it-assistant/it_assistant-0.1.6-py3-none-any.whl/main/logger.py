import os
import logging.config

config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'loggers': {
        'playground': {
            'handlers': ['log_agent', 'console', 'kafka_agent'],
            'propagate': False,
            'level': 'INFO',
        },
        'root': {
            'handlers': ['log_agent', 'console'],
            'level': 'INFO'
        }
    },
    'handlers': {
        'log_agent': {
            'level': 'INFO',
            'class': 'bytedlogger.StreamLogHandler',
            'tags': {
                'customtag': 'devops_boe',
            }
        },
        'kafka_agent': {
            'level': 'INFO',
            'class': 'kafkalogger.handlers.KafkaLogHandler',
            'formatter': 'default',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },

}
if os.getenv("DEBUG") == "true":
    config["handlers"].pop("kafka_agent")
    config["handlers"].pop("log_agent")
    config["loggers"]["playground"]["handlers"].remove("kafka_agent")
    config["loggers"]["playground"]["handlers"].remove("log_agent")
    config['loggers']['root']['handlers'].remove("log_agent")
logging.config.dictConfig(config)
logger = logging.getLogger('playground')
logging.getLogger("kafka").setLevel(logging.CRITICAL)
logging.getLogger("bytedkafka.common.config").setLevel(logging.ERROR)
logging.getLogger("kafka.producer.kafka").setLevel(logging.ERROR)
