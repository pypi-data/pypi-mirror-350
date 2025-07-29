from setuptools import setup

setup(
    name='odysseyaimodel',
    version='0.0.1',
    packages=['odyssey','odyssey.ai', 'odyssey.ai.model',  'odyssey.ai.model.cloud', 'odyssey.ai.model.cloud.core',
              'odyssey.ai.model.cloud.core.utilerias', 'odyssey.ai.model.cloud.core.seguridad',
              'odyssey.ai.model.cloud.core.models','odyssey.ai.model.cloud.core.handlers',
              'odyssey.ai.model.cloud.core.db',
              'odyssey.ai.model.cloud.core.log', 'odyssey.ai.model.cloud.configuracion'],
    url='http://devops:9001',
    license='License :: OSI Approved :: MIT License',
    author='AIT',
    author_email='noreply@odysseyaimodel.com',
    description='',
    install_requires = [ # Optional
      "requests","pycryptodome","paprika","json-encoder","pyctuator","python-dotenv","starlette","pytest-cov","pytest","pytz","oracledb",
        "httpx","PyJWT","python-dotenv","json-encoder","boto3","psycopg2-binary"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords = ["Odyssey", "Cobranza", "Cloud","Python","Template","Rest","Core","odyssey","odysseyai","odysseyaimodel"]  # Optional
)
