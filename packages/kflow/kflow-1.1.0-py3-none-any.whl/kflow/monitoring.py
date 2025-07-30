"""
Connection monitoring utilities for kflow ETL system
"""
import logging
from datetime import datetime
from kflow import authn

def get_connection_pool_stats(base_env: str = 'WarehouseProd'):
    """
    Get statistics about connection pool usage
    """
    try:
        engine = authn.getConnectionDB(base_env)
        pool = engine.pool
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'environment': base_env,
            'pool_size': pool.size(),
            'checked_in': pool.checkedin(),
            'checked_out': pool.checkedout(),
            'overflow': pool.overflow(),
            'pool_status': 'healthy' if pool.checkedin() > 0 else 'warning'
        }
        
        logging.info(f"Connection Pool Stats for {base_env}: {stats}")
        return stats
        
    except Exception as e:
        logging.error(f"Error getting connection pool stats: {str(e)}")
        return None

def test_redshift_connection():
    """
    Test Redshift connection and query performance
    """
    try:
        engine = authn.getConnectionDB('WarehouseProd')
        
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute("SELECT 1 as test")
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                logging.info("✅ Redshift connection test successful")
                return True
            else:
                logging.error("❌ Redshift connection test failed")
                return False
                
    except Exception as e:
        logging.error(f"❌ Redshift connection test failed: {str(e)}")
        return False

def check_long_running_queries(base_env: str = 'WarehouseProd'):
    """
    Check for long-running queries that might be causing locks
    """
    try:
        engine = authn.getConnectionDB(base_env)
        
        query = """
        SELECT 
            pid,
            user_name,
            db_name,
            query,
            starttime,
            DATEDIFF(second, starttime, GETDATE()) as duration_seconds
        FROM stv_recents 
        WHERE status = 'Running'
        AND DATEDIFF(second, starttime, GETDATE()) > 300
        ORDER BY starttime;
        """
        
        with engine.connect() as conn:
            result = conn.execute(query)
            long_queries = result.fetchall()
            
            if long_queries:
                logging.warning(f"Found {len(long_queries)} long-running queries (>5 minutes)")
                for query in long_queries:
                    logging.warning(f"PID {query[0]}: {query[5]}s - {query[3][:100]}...")
            else:
                logging.info("No long-running queries detected")
                
            return long_queries
            
    except Exception as e:
        logging.error(f"Error checking long-running queries: {str(e)}")
        return []

def cleanup_idle_connections():
    """
    Force cleanup of idle connections in the pool
    """
    try:
        from kflow.authn import _connection_pools
        
        for env_name, engine in _connection_pools.items():
            if hasattr(engine, 'pool'):
                # Force pool cleanup
                engine.pool.recreate()
                logging.info(f"Cleaned up connection pool for {env_name}")
                
    except Exception as e:
        logging.error(f"Error cleaning up connections: {str(e)}") 