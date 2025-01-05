import os
import requests
import json

class GTTGetPDFFromURLs:

# Function to get PDFs and save them into documents
    @staticmethod
    def get_pdfs():
        # JSON array containing descriptions and links

        pdf_data = [
            {
                "description": "White Paper 23-19: The Science Behind 23andMe’s Type 2 Diabetes Report",
                "link": "https://research.23andme.com/wp-content/uploads/2019/03/23_19-Type2Diabetes_March2019.pdf"
            },
            {
                "description": "White Paper 23-21: A Generalized Method for the Creation and Evaluation of Polygenic Scores",
                "link": "https://permalinks.23andme.com/pdf/23_21-PRSMethodology_May2020.pdf"
            },
            {
                "description": "Anxiety Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2022/12/Jamie-Anxiety-report-typical-likelihood.pdf"
            },
            {
                "description": "Asthma Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2022/12/asthma_typical-1.pdf"
            },
            {
                "description": "Atrial Fibrillation Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/Jamie-Atrial-Fibrillation-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Bipolar Disorder Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2024/06/bipolar-disorder-increased-1.pdf"
            },
            {
                "description": "Breast Cancer Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2024/03/Jamie-sample-report-breast-cancer-increased-likelihood.pdf"
            },
            {
                "description": "Colorectal Cancer Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2024/03/Jamie-sample-report-colorectal-cancer-increased-likelihood.pdf"
            },
            {
                "description": "Coronary Artery Disease Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2020/06/uploaded-Jamie-Coronary-Artery-Disease-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Diverticulitis Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Diverticulitis-typical-likelihood.pdf"
            },
            {
                "description": "Eczema (Atopic Dermatitis) Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/Jamie-Eczema-Atopic-Dermatitis-increased-likelihood-sample-report.pdf"
            },
            {
                "description": "Fibromyalgia Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2022/12/fibromyalgia_typical.pdf"
            },
            {
                "description": "Gallstones Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2021/11/uploaded-Jamie-Gallstones-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Gestational Diabetes Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Gestational-Diabetes-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Glaucoma Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Glaucoma-typical-likelihood-sample-report-10.35.15-AM.pdf"
            },
            {
                "description": "Gout Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Gout-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Hashimoto's Disease Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2022/12/Hashimoto.pdf"
            },
            {
                "description": "HDL Cholesterol Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-HDL-Cholesterol-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "High Blood Pressure Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-High-Blood-Pressure-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Insomnia Report",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/12/Jamie-sample-report-for-Insomnia-increased-likelihood.pdf"
            },
            {
                "description": "Irritable Bowel Syndrome",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Irritable-Bowel-Syndrome-typical-likelihood-sample-report-10.35.15-AM.pdf"
            },
            {
                "description": "Kidney Stones",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Kidney-Stones-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "LDL Cholesterol",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-LDL-Cholesterol-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Lupus",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/05/Jamie-lupus-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Migraine",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Migraine-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Nonalcoholic Fatty Liver Disease",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Nonalcoholic-Fatty-Liver-Disease-increased-likelihood-sample-report.pdf"
            },
            {
                "description": "Obstructive Sleep Apnea",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Obstructive-Sleep-Apnea-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Panic Attacks",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/06/Jamie-Panic-Attack-Typical-Likelihood-Sample-Report-.pdf"
            },
            {
                "description": "Polycystic Ovary Syndrome",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Polycystic-Ovary-Syndrome-increased-likelihood-sample-report.pdf"
            },
            {
                "description": "Preeclampsia",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-preeclampsia-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Prostate Cancer",
                "link": "https://medical.23andme.com/wp-content/uploads/2024/03/Jamie-sample-report-Prostate-Cancer-increased-likelihood.pdf"
            },
            {
                "description": "Psoriasis",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Psoriasis-increased-likelihood-sample-report-10.35.17-AM.pdf"
            },
            {
                "description": "Restless Legs Syndrome",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Restless-Legs-Syndrome-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Rosacea",
                "link": "https://medical.23andme.com/wp-content/uploads/2022/12/rosacea_typical.pdf"
            },
            {
                "description": "Severe Acne",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Severe-Acne-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Skin Cancer (Basal and Squamous Cell Carcinomas)",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Skin-Cancer-Basal-and-Squamous-Cell-Carcinomas-typical-risk-sample-report.pdf"
            },
            {
                "description": "Skin Cancer (Melanoma)",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Skin-Cancer-Melanoma-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Triglycerides",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Triglycerides-typical-likelihood-sample-report.pdf"
            },
            {
                "description": "Type 2 Diabetes",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/02/Jamie-Type-2-Diabetes-increased-likelihood-all-pages-of-sample-report.pdf"
            },
            {
                "description": "Uterine Fibroids",
                "link": "https://medical.23andme.com/wp-content/uploads/2023/01/uploaded-Jamie-Uterine-Fibroids-typical-likelihood-sample-report.pdf"
            }
            # You can extend this list with other objects from the original JSON array.
        ]

        # Directory where PDFs will be saved
        save_dir = './data/pdf'

        # Ensure the directory exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Function to download PDF
        def download_pdf(url, save_path):
            try:
                # Send a GET request to the URL
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for HTTP errors

                # Write the content to a PDF file
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded: {save_path}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")

        # Loop through the JSON array and download each PDF
        for item in pdf_data:
            # Generate a filename from the description (sanitize spaces and special chars)
            filename = item['description'].replace(":", "").replace(" ", "_") + ".pdf"
            save_path = os.path.join(save_dir, filename)
            
            # Download the PDF
            download_pdf(item['link'], save_path)
