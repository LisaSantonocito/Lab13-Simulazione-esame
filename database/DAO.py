from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllEdge(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from neighbor n where n.state1<n.state2 group by n.state1, n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((idMap[row["state1"]],idMap[row["state2"]]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgeW(idMap, year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1, n.state2, count(*) as peso  from sighting s , neighbor n where (n.state1=s.state or n.state2=s.state) and n.state1 < n.state2 and year(s.`datetime`) = %s and s.shape = %s group by n.state1, n.state2   """

        cursor.execute(query, (year,shape))

        for row in cursor:
            result.append((idMap[row["state1"]], idMap[row["state2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYear():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime`) as anno  from sighting s   order by `datetime` """
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllForme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape  from sighting s where shape != "" and year(s.`datetime`)=%s"""
        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllState():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *  from state s """
        cursor.execute(query, ())

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result
