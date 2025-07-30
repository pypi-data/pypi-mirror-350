# Seatools-starter-sqlalchemy

The SQLAlchemy starter for seatools ioc.

[中文文档](./README_zh.md)

## Repository Addresses:
1. https://github.com/seatools-py/seatools-starter-sqlalchemy
2. https://gitee.com/seatools-py/seatools-starter-sqlalchemy

## Usage Guide
1. Install with `poetry add seatools-starter-sqlalchemy`
2. Configure the `config/application.yml` file as follows:
```yaml
# seatools configuration
seatools:
  # sqlalchemy configuration
  sqlalchemy:
    echo: false
    pool_cycle: 3600
  # database configuration
  datasource:
    # database bean name
    demo_db:
      host: xxx
      port: 1234
      user: xxx
      password: sss
      database: xxx
      driver: sqlite # sqlalchemy schema database driver, examples: sqlite+aiosqlite (asynchronous), mysql+pymysql, hive, clickhouse, etc.
      primary: false # whether it is the default bean
      is_async: false # whether it is asynchronous, if the driver is asynchronous then this value needs to be set to true
      # override configuration for individual databases' sqlalchemy
      config:
        echo: true
        # 1.0.6 version supports custom Session, default synchronous is sqlalchemy.orm.Session, asynchronous is sqlalchemy.ext.asyncio.AsyncSession
        session_cls: sqlalchemy.orm.Session # can be changed to other Sessions, for example: sqlmodel.orm.Session (sqlmodel needs to be installed)
```
3. Usage example:
```python
from seatools.ioc import run, Autowired
from seatools.sqlalchemy.decorators.ioc import new_session
from sqlalchemy.orm import Session
from seatools.sqlalchemy import SqlAlchemyClient


# Start ioc
run(scan_package_names=['seatools.ioc.starters.sqlalchemy'], config='./config')

"""
Method one, using decorator, recommended
"""
@new_session
def xxx(session: Session):
    ...

# Call
xxx()


# Method two, not recommended
client = Autowired(cls=SqlAlchemyClient)

with client.session() as session:
    ...
```
