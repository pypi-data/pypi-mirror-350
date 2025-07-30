from typing import Callable

from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from sqlalchemy.orm import sessionmaker


class SQLAlchemySessionOperator(PythonOperator):
    def __init__(
            self, conn_id: str, python_callable: Callable, *args, **kwargs
    ):
        super().__init__(*args, python_callable=python_callable, **kwargs)
        self.conn_id = conn_id

    def get_session_factory(self) -> sessionmaker:
        hook = MySqlHook(self.conn_id)
        engine = hook.get_sqlalchemy_engine()

        return sessionmaker(bind=engine)

    def execute_callable(self):
        session_factory = self.get_session_factory()

        with session_factory() as session:
            try:
                result = self.python_callable(
                    *self.op_args, session=session, **self.op_kwargs
                )
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()
        return result
