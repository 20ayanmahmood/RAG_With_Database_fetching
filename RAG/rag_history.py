import cx_Oracle
# import oracledb
import RAG_API


def create_connection():
    try:
        conn = cx_Oracle.connect("makess/makess@192.168.5.136:1521/orcl")
        # connection = oracledb.connect(
        #     user="makess",
        #     password="makess",
        #     dsn="localhost:1521/orcl"
        # )
        RAG_API.logger.info("Connection Establised Succesfully")
        return conn
    except oracledb.Error as e:
        RAG_API.logger.error(f"Error connecting to database: {e}")
        return None

def history(question,session_id,answer,token,time,user_id,date):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO rag_history (question, session_id, tokens, time_in_secs,user_id,conversation_date,answer)
        VALUES (:question, :session_id, :tokens, :time_in_secs,:user_id,:conversation_date,:answer)
        """
        data = {
            "question": question,
            "session_id": session_id,
            "answer": answer,
            "tokens": token,
            "time_in_secs": time,
            "user_id":user_id,
            "conversation_date":date
        }
        try:
            cursor.execute(insert_query, data)
            connection.commit()
            RAG_API.logger.info(f"Data Inserted Succesfully:{data}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print("Error code:", error.code)
            print("Error message:", error.message)
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()
    except Exception as e:
        return f"Error While Storing History:{e}"

