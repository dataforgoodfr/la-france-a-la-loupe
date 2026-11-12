set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# dlt's ingestion pipelines
pipeline name:
    uv run --directory pipelines python -m {{name}}.{{name}}_pipeline

education_pipeline: (pipeline "education")
transverse_pipeline: (pipeline "transverse")
#immigration_pipeline: (pipeline "immigration")
sante_pipeline: (pipeline "sante")
agriculture_pipeline: (pipeline "agriculture")
securite_pipeline: (pipeline "securite")

# Lance tous les pipelines en parallele (logs entremeles : lancer un pipeline seul pour deboguer)
[parallel]
pipelines: (pipeline "education") (pipeline "transverse") (pipeline "sante") (pipeline "agriculture") (pipeline "securite")

# dbt (ex. just dbt build -t dev_s3). Chemins absolus vers ./data pour le target dev.
dbt *args:
    mkdir -p "{{justfile_directory()}}/data/dev/warehouse" "{{justfile_directory()}}/data/dev/database" "{{justfile_directory()}}/data/dev_s3/database"
    LFE4_DATA_DIR="{{justfile_directory()}}/data" uv run --directory dbt/lfe4 dbt {{args}}

# Ingestion dlt puis build dbt, avec le meme profil (ex. just run dev_s3)
run profile="dev":
    WORKSPACE__PROFILE={{profile}} just pipelines
    just dbt build -t {{profile}}

# Supprime les donnees locales (lake + warehouse) et l'etat dlt d'un profil. Ne touche pas au S3.
[confirm("Supprimer data/<profil> et pipelines/.dlt/state/<profil> ?")]
clean profile="dev":
    rm -rf "{{justfile_directory()}}/data/{{profile}}" "{{justfile_directory()}}/pipelines/.dlt/state/{{profile}}"

parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force

# launch webapp (pmtiles lus dans webapp/public/data, ou ailleurs : just webapp http://lfe4.web.lfe4.localhost:3902/pmtiles)
webapp pmtiles_url="":
    cd webapp && {{ if pmtiles_url == "" { "" } else { "NEXT_PUBLIC_PMTILES_URL=" + pmtiles_url } }} npm run dev

# Expose le bucket Garage local en lecture anonyme (port 3902) avec le CORS requis par pmtiles
garage_web:
    docker exec garage /garage bucket website --allow lfe4
    AWS_ACCESS_KEY_ID=garagekeyid AWS_SECRET_ACCESS_KEY=garagesecretchangethis AWS_DEFAULT_REGION=lfe4 \
        aws s3api put-bucket-cors --bucket lfe4 --endpoint-url http://localhost:3900 --cors-configuration \
        '{"CORSRules":[{"AllowedOrigins":["*"],"AllowedMethods":["GET","HEAD"],"AllowedHeaders":["range","if-match"],"ExposeHeaders":["etag","content-range","content-length"],"MaxAgeSeconds":3600}]}'
