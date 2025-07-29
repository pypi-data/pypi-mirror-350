class ArcGISConfig:
    """
    Clase contenedora de configuración necesaria para la conexión con los servicios de ArcGIS.
    Se utiliza como objeto de configuración para inicializar un ArcGISClient.

    Parámetros:
        url_token_provider: URL del servicio para obtener el token de autenticación.
        username: Usuario para autenticarse en el servicio de tokens de ArcGIS.
        password: Contraseña asociada al usuario.
        format: Formato en el que se espera la respuesta del servidor (por ejemplo, "json").
        referer: Referencia requerida por algunos servidores ArcGIS para validar el origen de la solicitud.
        expiration: Tiempo de expiración (en minutos) del token generado.
        url_geoportal: URL base del geoportal de ArcGIS donde se interactuará con los datos.
        endpoint_api_features: Endpoint del API de ArcGIS, relacionado con los features.
        true_curve: Parámetro booleano que indica si se deben mantener las curvas al enviar geometrías.
    """

    def __init__(self, url_token_provider, username, password, format, referer, expiration, url_geoportal, endpoint_api_features, true_curve):
        self.url_token_provider = url_token_provider
        self.username = username
        self.password = password
        self.format = format
        self.referer = referer
        self.expiration = expiration
        self.url_geoportal = url_geoportal
        self.endpoint_api_features = endpoint_api_features
        self.true_curve = true_curve
