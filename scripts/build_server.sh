#!/bin/bash

# Check if the server group parameter is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <server_group>"
  exit 1
fi

# Assign the server group parameter
SERVER_GROUP="$1"

# Define the source and destination directories
BASE_TEMPLATE_DIR="base_template"
DESTINATION_DIR="servers/$SERVER_GROUP"

# Check if the base_template directory exists
if [ ! -d "$BASE_TEMPLATE_DIR" ]; then
  echo "Source directory '$BASE_TEMPLATE_DIR' does not exist."
  exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$DESTINATION_DIR"

# Copy all files from the base template to the destination directory
cp -R "$BASE_TEMPLATE_DIR/"* "$DESTINATION_DIR/"
echo "All files from '$BASE_TEMPLATE_DIR' have been copied to '$DESTINATION_DIR'."

####################
python scripts/build_requirements.py "$SERVER_GROUP"

####################
# Define the source and destination file paths for requirements
SOURCE_FILE="requirements/${SERVER_GROUP}_requirements.txt"
DESTINATION_FILE="servers/$SERVER_GROUP/application/rakam_systems/requirements.txt"
cat "$SOURCE_FILE" > "$DESTINATION_FILE"
echo "Content of $DESTINATION_FILE has been replaced with content from $SOURCE_FILE."

####################
# Specify the folder you want to delete
FOLDER_PATH="requirements"

# Check if the folder exists
if [ -d "$FOLDER_PATH" ]; then
  # Delete the folder and its contents
  rm -r "$FOLDER_PATH"
  echo "Folder deleted: $FOLDER_PATH"
else
  echo "Folder does not exist: $FOLDER_PATH"
fi

####################
# Path to the setup.cfg and requirements.txt
CFG_FILE="servers/$SERVER_GROUP/application/rakam_systems/setup.cfg"
REQ_FILE="servers/$SERVER_GROUP/application/rakam_systems/requirements.txt"

# Backup the original setup.cfg
cp "$CFG_FILE" "${CFG_FILE}.bak"

# Use awk to replace the install_requires section in setup.cfg
awk '
    BEGIN {
        # Read requirements.txt into an array
        while ((getline line < "'$REQ_FILE'") > 0) {
            reqs[i++] = "    " line
        }
        close("'$REQ_FILE'")
    }
    /^install_requires/ {
        print "install_requires ="
        in_section = 1
        for (j = 0; j < i; j++) {
            print reqs[j]
        }
        next
    }
    in_section && /^    / { next } # Skip existing install_requires entries
    in_section && !/^    / { in_section = 0 }
    { print }
' "$CFG_FILE" > tmp.cfg && mv tmp.cfg "$CFG_FILE"

echo "install_requires in setup.cfg updated with contents from requirements.txt."

####################
python scripts/build_components.py "$SERVER_GROUP"

# Define the source and destination file paths for components
SOURCE_FILE="generated_components.py"
DESTINATION_FILE="servers/$SERVER_GROUP/application/engine/components.py"
cat "$SOURCE_FILE" > "$DESTINATION_FILE"
rm -f generated_components.py

####################
python scripts/build_app.py "$SERVER_GROUP"

####################
# Define source and destination files for various app files
for FILE in urls.py views.py serializers.py; do
  SOURCE_FILE="$FILE"
  DESTINATION_FILE="servers/$SERVER_GROUP/application/$FILE"
  cat "$SOURCE_FILE" > "$DESTINATION_FILE"
  rm -f "$SOURCE_FILE"
done
