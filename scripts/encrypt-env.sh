#!/bin/bash

set -eu

ENVIRONMENT=$1

case $ENVIRONMENT in
"production")
  PROJECT=srandom ;;
*)
  echo "encrypt-env.sh {production}"
  exit 1 ;;
esac

gcloud kms encrypt --location asia-northeast1 --keyring app --key env --project $PROJECT --plaintext-file ./deployments/"$ENVIRONMENT"/.env."$ENVIRONMENT" --ciphertext-file ./deployments/"$ENVIRONMENT"/.env.enc
