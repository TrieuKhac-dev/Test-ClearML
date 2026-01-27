
#!/bin/sh
# Parse REMOTE_NAME=<name>
DVC_REMOTE_NAME=""
for arg in "$@"; do
  case $arg in
    REMOTE_NAME=*)
      DVC_REMOTE_NAME="${arg#*=}"
      ;;
    *)
      # Ignore all other args (including --)
      ;;
  esac
done

set -a
[ -f .env ] && . .env
set +a

if [ -z "$DVC_REMOTE_NAME" ]; then
  echo "Please export DVC_REMOTE_NAME or pass REMOTE_NAME=<name> as an argument!"
  exit 1
fi

remote_var=$(echo "$DVC_REMOTE_NAME" | tr '[:lower:]' '[:upper:]' | tr '-' '_')

access_key_var="DVC_${remote_var}_ACCESS_KEY_ID"
secret_key_var="DVC_${remote_var}_SECRET_ACCESS_KEY"
endpoint_var="DVC_${remote_var}_ENDPOINT_URL"

access_key=$(eval echo \$$access_key_var)
secret_key=$(eval echo \$$secret_key_var)
endpoint=$(eval echo \$$endpoint_var)

dvc remote modify --local "$DVC_REMOTE_NAME" access_key_id "$access_key"
dvc remote modify --local "$DVC_REMOTE_NAME" secret_access_key "$secret_key"
dvc remote modify --local "$DVC_REMOTE_NAME" endpointurl "$endpoint"