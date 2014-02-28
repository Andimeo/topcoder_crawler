from MySQLdb import connect

def init():
	conn = connect('162.105.146.32', 'root', 'webg1220', 'topcoder')
	cur = conn.cursor()
	return conn, cur

def close(conn):
	conn.close()

	
