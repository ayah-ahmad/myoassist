import xml.etree.ElementTree as ET
import numpy as np

def interpolate_params(easy_xml, realistic_xml, output_xml, alpha=0.5):
    """
    Interpolate muscle parameters between an 'easy' and 'realistic' XML.

    Args:
        easy_xml (str): path to easy muscle XML
        realistic_xml (str): path to realistic muscle XML
        output_xml (str): where to save interpolated XML
        alpha (float): interpolation factor, 0 = easy, 1 = realistic
    """
    # Load both XML trees
    tree_easy = ET.parse(easy_xml)
    tree_real = ET.parse(realistic_xml)

    root_easy = tree_easy.getroot()
    root_real = tree_real.getroot()

    # Iterate over muscles (general actuators with class="muscle")
    for m_easy, m_real in zip(root_easy.findall(".//general[@class='muscle']"),
                              root_real.findall(".//general[@class='muscle']")):
        # Interpolate gainprm and biasprm
        for prm in ["gainprm", "biasprm"]:
            vals_easy = np.array(list(map(float, m_easy.get(prm).split())))
            vals_real = np.array(list(map(float, m_real.get(prm).split())))
            vals_interp = (1 - alpha) * vals_easy + alpha * vals_real
            m_easy.set(prm, " ".join(f"{v:.6g}" for v in vals_interp))

        # Interpolate lengthrange (if present)
        if m_easy.get("lengthrange") and m_real.get("lengthrange"):
            vals_easy = np.array(list(map(float, m_easy.get("lengthrange").split())))
            vals_real = np.array(list(map(float, m_real.get("lengthrange").split())))
            vals_interp = (1 - alpha) * vals_easy + alpha * vals_real
            m_easy.set("lengthrange", " ".join(f"{v:.6g}" for v in vals_interp))

    # Save new XML
    tree_easy.write(output_xml)
    print(f"Saved interpolated XML → {output_xml} (alpha={alpha:.2f})")

# Example usage
if __name__ == "__main__":
    # Paths to your files
    easy = "myolegs_muscle_easy.xml"
    real = "myolegs_muscle_restricted.xml"

    # Generate several interpolation steps
    for a in [0.0, 0.25, 0.5, 0.75, 1.0]:
        out = f"myolegs_muscle_interp_{a:.2f}.xml"
        interpolate_params(easy, real, out, alpha=a)
