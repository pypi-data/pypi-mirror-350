from starlette.requests import HTTPConnection

class BaseExtractors:
    @staticmethod
    def extract_client_ip(conn:HTTPConnection) -> str:
        """Extract client IP with more robust handling of proxies"""
        #* Check for X-Forwarded-For header (common when behind proxy/load balancer)
        x_forwarded_for = conn.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            #* The client's IP is the first one in the list
            ips = [ip.strip() for ip in x_forwarded_for.split(",")]
            return ips[0]

        #* Check for X-Real-IP header (used by some proxies)
        x_real_ip = conn.headers.get("X-Real-IP")
        if x_real_ip:
            return x_real_ip

        #* Fall back to direct client connection
        return conn.client.host if conn.client else "unknown"