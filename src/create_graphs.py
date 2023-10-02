import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Create a dataframe from the provided values
data = {
    "lang": ["de", "en", "fi", "fr", "hu", "it", "pl", "sl"],
    "count": [127, 237, 104, 174, 4, 230, 2, 103]
}
df = pd.DataFrame(data)

# Create a color palette
palette = sns.color_palette("hls", len(data["lang"]))

# Create a bar chart
plt.figure(figsize=(10,6))
ax = sns.barplot(x="lang", y="count", data=df, palette=palette)

# Annotate each bar with its respective count
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 9), 
                textcoords='offset points')

plt.title("Samples per Language")
plt.ylabel("Samples")
plt.xlabel("Language")

# Specify the output path directly
output_path = "C:/Users/Alice/Desktop/Code/EPTIC/docs/lang_counts.png"
plt.savefig(output_path)

plt.show()
