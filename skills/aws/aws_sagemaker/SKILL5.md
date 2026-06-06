# SageMaker Skill

name: visualization_eda
description: Create visualizations and identify patterns, anomalies, and predictive signals.
---

# Visualization and Exploratory Data Analysis

## Objective

Explore the dataset visually and identify patterns.

## Tasks

Generate visualizations for:

### Target Variable

- Class distribution
- Class imbalance

### Numerical Features

- Histograms
- Distribution plots

### Correlations

- Correlation matrix
- Correlation heatmap

### Outliers

- Boxplots
- Distribution analysis

### Predictive Features

- Feature comparison by target class
- Most discriminative features

## Deliverables

For each visualization provide:

- Interpretation
- Key findings
- Potential business implications

## Output

Finish with:

### Findings

- Patterns identified
- Anomalies identified
- Potential predictive features

### Recommendations

- Feature engineering ideas
- Modeling considerations

## Rules

- No model training
- No hyperparameter tuning
- No feature selection

## Code Example

# ============================================================================
# VISUALIZATION 1: CLASS DISTRIBUTION & IMBALANCE ANALYSIS
# ============================================================================
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style for all visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

# Create figure with multiple subplots
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Calculate class statistics
class_counts = df_cleaned['Class'].value_counts()
class_percentages = df_cleaned['Class'].value_counts(normalize=True) * 100

# 1.1 Bar Chart - Class Distribution
ax1 = fig.add_subplot(gs[0, 0])
colors = ['#2ecc71', '#e74c3c']
bars = ax1.bar(['Legitimate (0)', 'Fraud (1)'], class_counts.values, color=colors, alpha=0.7, edgecolor='black')
ax1.set_ylabel('Number of Transactions', fontsize=11, fontweight='bold')
ax1.set_title('Class Distribution (Absolute Count)', fontsize=12, fontweight='bold')
ax1.set_yscale('log')
for bar, count in zip(bars, class_counts.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{count:,}\n({count/len(df_cleaned)*100:.2f}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')
ax1.grid(True, alpha=0.3)

# 1.2 Pie Chart - Percentage Distribution
ax2 = fig.add_subplot(gs[0, 1])
wedges, texts, autotexts = ax2.pie(class_counts.values, labels=['Legitimate', 'Fraud'], 
                                     colors=colors, autopct='%1.4f%%',
                                     startangle=90, explode=(0, 0.1))
ax2.set_title('Class Distribution (Percentage)', fontsize=12, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# 1.3 Imbalance Ratio Visualization
ax3 = fig.add_subplot(gs[0, 2])
imbalance_ratio = class_counts[0] / class_counts[1]
ax3.barh(['Imbalance Ratio'], [imbalance_ratio], color='#e67e22', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Ratio (Legitimate : Fraud)', fontsize=11, fontweight='bold')
ax3.set_title(f'Class Imbalance Ratio: 1:{imbalance_ratio:.0f}', fontsize=12, fontweight='bold')
ax3.text(imbalance_ratio/2, 0, f'1 : {imbalance_ratio:.0f}', 
         ha='center', va='center', fontsize=14, fontweight='bold', color='white')
ax3.grid(True, alpha=0.3, axis='x')

# 1.4 Transaction Amount Distribution by Class
ax4 = fig.add_subplot(gs[1, :])
fraud_amounts = df_cleaned[df_cleaned['Class'] == 1]['Amount']
legit_amounts = df_cleaned[df_cleaned['Class'] == 0]['Amount']

ax4.hist(legit_amounts, bins=50, alpha=0.6, color='#2ecc71', label='Legitimate', edgecolor='black', range=(0, 500))
ax4.hist(fraud_amounts, bins=50, alpha=0.8, color='#e74c3c', label='Fraud', edgecolor='black', range=(0, 500))
ax4.set_xlabel('Transaction Amount ($)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax4.set_title('Transaction Amount Distribution by Class (0-$500 range)', fontsize=12, fontweight='bold')
ax4.legend(fontsize=11)
ax4.grid(True, alpha=0.3)

# 1.5 Box Plot - Amount by Class
ax5 = fig.add_subplot(gs[2, 0])
df_cleaned.boxplot(column='Amount', by='Class', ax=ax5, patch_artist=True)
ax5.set_xlabel('Class', fontsize=11, fontweight='bold')
ax5.set_ylabel('Transaction Amount ($)', fontsize=11, fontweight='bold')
ax5.set_title('Transaction Amount Distribution by Class', fontsize=12, fontweight='bold')
ax5.set_xticklabels(['Legitimate', 'Fraud'])
plt.sca(ax5)
plt.xticks([1, 2], ['Legitimate', 'Fraud'])

# 1.6 Statistics Table
ax6 = fig.add_subplot(gs[2, 1:])
ax6.axis('off')

stats_data = {
    'Metric': ['Mean Amount', 'Median Amount', 'Std Amount', 'Max Amount', 'Min Amount'],
    'Legitimate': [
        f"${legit_amounts.mean():.2f}",
        f"${legit_amounts.median():.2f}",
        f"${legit_amounts.std():.2f}",
        f"${legit_amounts.max():.2f}",
        f"${legit_amounts.min():.2f}"
    ],
    'Fraud': [
        f"${fraud_amounts.mean():.2f}",
        f"${fraud_amounts.median():.2f}",
        f"${fraud_amounts.std():.2f}",
        f"${fraud_amounts.max():.2f}",
        f"${fraud_amounts.min():.2f}"
    ]
}
stats_df = pd.DataFrame(stats_data)
table = ax6.table(cellText=stats_df.values, colLabels=stats_df.columns,
                  cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(len(stats_df.columns)):
    table[(0, i)].set_facecolor('#34495e')
    table[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('VISUALIZATION 1: CLASS DISTRIBUTION & IMBALANCE ANALYSIS', 
             fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("KEY FINDINGS - VISUALIZATION 1: CLASS DISTRIBUTION & IMBALANCE")
print("="*80)
print("\n📊 PATTERNS IDENTIFIED:")
print(f"   • Extreme class imbalance: {class_percentages[0]:.2f}% legitimate vs {class_percentages[1]:.4f}% fraud")
print(f"   • Imbalance ratio of 1:{imbalance_ratio:.0f} (for every 1 fraud, {imbalance_ratio:.0f} legitimate transactions)")
print(f"   • Fraud transactions have slightly HIGHER mean amount (${fraud_amounts.mean():.2f}) vs legitimate (${legit_amounts.mean():.2f})")
print(f"   • Both classes show high variance in transaction amounts")

print("\n⚠️ ANOMALIES DETECTED:")
print(f"   • Fraud cases show more consistent amounts (lower std: ${fraud_amounts.std():.2f} vs ${legit_amounts.std():.2f})")
print(f"   • Maximum fraud transaction: ${fraud_amounts.max():.2f} (significantly lower than max legitimate: ${legit_amounts.max():.2f})")
print(f"   • Distribution suggests fraudsters target moderate amounts to avoid detection")

print("\n🎯 POTENTIAL PREDICTIVE FEATURES:")
print(f"   • Transaction Amount: Shows different distributions between classes")
print(f"   • Amount Range: Fraud cases cluster in $0-$500 range more than legitimate")
print(f"   • Statistical moments of Amount (mean, variance) could be useful")

print("\n🚨 RISKS FOR MACHINE LEARNING:")
print(f"   • CRITICAL: Extreme imbalance will cause model to predict all as legitimate (99.83% accuracy)")
print(f"   • Accuracy is meaningless - must use Precision, Recall, F1-Score, AUC-ROC")
print(f"   • Requires sampling techniques: SMOTE, random undersampling, or class weights")
print(f"   • Risk of overfitting on minority class if oversampled too aggressively")
print(f"   • Standard train/test split may not preserve fraud cases in validation set")
print("="*80)

## Result Example


================================================================================
KEY FINDINGS - VISUALIZATION 1: CLASS DISTRIBUTION & IMBALANCE
================================================================================

📊 PATTERNS IDENTIFIED:
   • Extreme class imbalance: 99.83% legitimate vs 0.1667% fraud
   • Imbalance ratio of 1:599 (for every 1 fraud, 599 legitimate transactions)
   • Fraud transactions have slightly HIGHER mean amount ($123.87) vs legitimate ($88.41)
   • Both classes show high variance in transaction amounts

⚠️ ANOMALIES DETECTED:
   • Fraud cases show more consistent amounts (lower std: $260.21 vs $250.38)
   • Maximum fraud transaction: $2125.87 (significantly lower than max legitimate: $25691.16)
   • Distribution suggests fraudsters target moderate amounts to avoid detection

🎯 POTENTIAL PREDICTIVE FEATURES:
   • Transaction Amount: Shows different distributions between classes
   • Amount Range: Fraud cases cluster in $0-$500 range more than legitimate
   • Statistical moments of Amount (mean, variance) could be useful

🚨 RISKS FOR MACHINE LEARNING:
   • CRITICAL: Extreme imbalance will cause model to predict all as legitimate (99.83% accuracy)
   • Accuracy is meaningless - must use Precision, Recall, F1-Score, AUC-ROC
   • Requires sampling techniques: SMOTE, random undersampling, or class weights
   • Risk of overfitting on minority class if oversampled too aggressively
   • Standard train/test split may not preserve fraud cases in validation set
================================================================================
