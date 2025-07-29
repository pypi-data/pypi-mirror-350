from vlcishared.tokens.token_provider import TokenProvider


class ArcGISTokenProvider(TokenProvider):
    """
    Proveedor de tokens específico para servicios ArcGIS.
    Extiende la clase base TokenProvider.

    Parámetros:
        url (str): URL del endpoint de autenticación de ArcGIS.
        username (str): Nombre de usuario para autenticación.
        password (str): Contraseña del usuario.
        format (str): Formato de la respuesta (por ejemplo, 'json').
        referer (str): Referer requerido por el servicio ArcGIS.
        expiration (int): Duración del token en minutos.

    Al instanciarse, intenta obtener el token automáticamente.
    """

    def __init__(self, url, username, password, format, referer, expiration):
        super().__init__(url)
        self.username = username
        self.password = password
        self.format = format
        self.referer = referer
        self.expiration = expiration

    def obtener_token(self):
        """
        Realiza la solicitud del token al servidor ArcGIS usando las credenciales
        y parámetros configurados. Asigna el token recibido a self.token.

        Lanza:
            ValueError: Si la respuesta no contiene un token válido.
        """
        payload = {
            "username": self.username,
            "password": self.password,
            "f": self.format,
            "referer": self.referer,
            "expiration": self.expiration,
        }
        respuesta = self._solicitar_nuevo_token(data=payload)
        token = respuesta.get("token")
        if token is None:
            raise ValueError("No se ha podido obtener el token.")
        self.token = token
