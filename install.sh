#!/usr/bin/env bash
set -e

# ANSI color codes
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
CYAN="\e[36m"
RESET="\e[0m"
BOLD="\e[1m"
CHECK="${GREEN}✔${RESET}"
CROSS="${RED}✘${RESET}"

MODEL_DIR="./nails/models"
mkdir -p "$MODEL_DIR"

declare -A models=(
  [efficientnetv2s_epoch5.pth]="https://huggingface.co/shibarashii/nail-disease-detection/resolve/main/models/efficientnetv2s/weights/efficientnetv2s_epoch5.pth"
  [regnety16gf_epoch5.pth]="https://huggingface.co/shibarashii/nail-disease-detection/resolve/main/models/regnety16gf/weights/regnety16gf_epoch5.pth"
  [swinv2b_epoch5.pth]="https://huggingface.co/shibarashii/nail-disease-detection/resolve/main/models/swinv2b/weights/swinv2b_epoch5.pth"
  [resnet50_epoch5.pth]="https://huggingface.co/shibarashii/nail-disease-detection/resolve/main/models/resnet50/weights/resnet50_epoch5.pth"
)

echo -e "${CYAN}${BOLD}🔽 Downloading model weights...${RESET}"
for filename in "${!models[@]}"; do
  echo -e "${YELLOW}Downloading ${filename}...${RESET}"
  wget -q --show-progress -O "$MODEL_DIR/$filename" "${models[$filename]}" \
    && echo -e "  ${CHECK} ${GREEN}${filename} downloaded successfully.${RESET}" \
    || echo -e "  ${CROSS} ${RED}Failed to download ${filename}.${RESET}"
done

echo -e "\n${GREEN}${BOLD}✅ Models installed successfully!${RESET}\n"

echo -e "${CYAN}${BOLD}Next steps:${RESET}\n"

echo -e "${YELLOW}1.${RESET} Create a virtual environment:"
echo -e "   ${BOLD}python -m venv .venv${RESET}\n"

echo -e "${YELLOW}2.${RESET} Activate it:"
echo -e "   ${BOLD}# On Linux/Mac:${RESET}    . .venv/bin/activate"
echo -e "   ${BOLD}# On Windows:${RESET}      . .venv/Scripts/activate\n"

echo -e "${YELLOW}3.${RESET} Install dependencies:"
echo -e "   ${BOLD}python -m pip install -r requirements.txt${RESET}\n"

echo -e "${YELLOW}4.${RESET} Apply database migrations:"
echo -e "   ${BOLD}python manage.py migrate${RESET}\n"

echo -e "${YELLOW}5.${RESET} (Optional) Create a Django superuser for admin access:"
echo -e "   ${BOLD}python manage.py createsuperuser${RESET}\n"

echo -e "${YELLOW}6.${RESET} Run the development server:"
echo -e "   ${BOLD}python manage.py runserver${RESET}\n"
