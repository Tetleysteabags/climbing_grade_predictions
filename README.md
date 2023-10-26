# The Impact of Strength Metrics on Climbing Performance

In recent years companies such as Lattice have begun using data analytics to inform climbers of where their potential weaknesses are to better personalise training plans (and hopefully improve long term performance).

Many of these datasets are not publicly available, but the team at Power Company Climbing have been kind enough to share theirs.

In this notebook I am using a dataset from Power Company Climbing which contains around 600 self reported members, providing a variety of climbing benchmarks. The goal of the workbook is to test different machine learning models to determine which metrics play the largest role in climbing performance, and whether we can use this data to then predict climbing grades.

The workbook splits out bouldering and sport climbing and performs the analysis on these two variations of climbing separately, using Linear Regression, Random Forest, and Gradient Boosting models. The models are saved in pkl files and then used in Streamlit to create a simple UI where users can input their strength metrics and receive an estimated max grade for bouldering and sport climbing.