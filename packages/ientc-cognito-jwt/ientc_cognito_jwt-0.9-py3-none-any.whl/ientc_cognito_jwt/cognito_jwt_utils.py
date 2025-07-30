import httpx
import datetime
from jose import jwt, jws, JWTError


def validate_jwt(token: str, aws_user_pool_id: str, aws_region: str, audience: str | None = None):
    """ Perform the token validation steps as per
    https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html

    :param token: jwt string
    :param aws_user_pool_id: Cognito User Pool ID
    :param aws_region: AWS region
    :param audience: Optional audience to check against the token's aud claim.
    :return: True if validation succeeds; False otherwise, a error message and the decoded token.
    :rtype: tuple(bool, str, dict)
    """

    def result(msg=None, decoded=None):
        return (True, None, decoded) if msg is None else (False, msg, None)

    # Default Issuer
    issuer = f"https://cognito-idp.{aws_region}.amazonaws.com/{aws_user_pool_id}"

    # Get Cognito JKWS json data.
    userpool_keys = httpx.get(
        f"https://cognito-idp.{aws_region}.amazonaws.com/"
        f"{aws_user_pool_id}/.well-known/jwks.json"
    )

    # Check if the request is successful
    if userpool_keys.status_code != 200:
        return result("Failed to get keys")

    userpool_keys = userpool_keys.json()

    # 2 Decode the token string into JWT format.
    try:
        jwt_headers = jwt.get_unverified_header(token)
    except JWTError as jwt_err:
        return result(str(jwt_err))
    kid = jwt_headers["kid"]

    use_keys = [key for key in userpool_keys["keys"] if key["kid"] == kid]
    if len(use_keys) != 1:
        return result("Obtained keys are wrong")
    use_key = use_keys[0]
    try:
        if audience is not None:
            decoded = jwt.decode(token, use_key, audience=audience)
        else:
            decoded = jwt.decode(token, use_key)
    except JWTError as e:
        return result("Failed to decode token: {}".format(e))

    # 3 Check iss claim
    claims = jwt.get_unverified_claims(token)
    if claims["iss"] != issuer:
        return result("Invalid issuer in token")

    # 4 Check token use
    # Should we only allow one of the tokens or both "id" and "access"?
    if claims["token_use"] not in ["id", "access"]:
        return result("Token not of valid use")

    # 5 Check kid
    jwk_kids = [obj["kid"] for obj in userpool_keys["keys"]]
    if kid not in jwk_kids:
        # Should be here; condition 2 should have guaranteed this
        return result("Token is not related to id provider")

    # 6 Verify signature of decoded JWT?
    try:
        jws.verify(token, use_key, jwt_headers["alg"])
    except JWTError as e:
        return result("Failed to verify signature {}".format(e))

    # 7 Check exp and make sure it is not expired
    exp = claims["exp"]
    exp_date = datetime.datetime.fromtimestamp(exp)
    now = datetime.datetime.now()
    if exp_date < now:
        return result("Token has expired {}".format(exp_date - now))

    return result(None, decoded)
