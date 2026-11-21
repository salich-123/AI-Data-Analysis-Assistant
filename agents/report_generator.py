
def generate_report(df):

    print("\n========== GENERATING REPORT ==========")

    report = []

    report.append("AI DATA ANALYSIS ASSISTANT")
    report.append("==========================")
    
    # 1. Dataset information
    report.append("\n1. DATASET INFORMATION")
    report.append(f"Total Rows: {df.shape[0]}")
    report.append(f"Total Columns: {df.shape[1]}")

    # 2. Data quality
    report.append("\n2. DATA QUALITY")
    report.append(f"Missing Values: {df.isnull().sum().sum()}")
    report.append(f"Duplicate Rows: {df.duplicated().sum()}")

    # 3. Numerical analysis
    report.append("\n3. NUMERICAL ANALYSIS")

    if "Marks" in df.columns:
        report.append(f"Average Marks: {df['Marks'].mean():.2f}")
        report.append(f"Highest Marks: {df['Marks'].max()}")
        report.append(f"Lowest Marks: {df['Marks'].min()}")

    if "Salary" in df.columns:
        report.append(f"Average Salary: {df['Salary'].mean():.2f}")

    # 4. Student performance
    if "Name" in df.columns and "Marks" in df.columns:

        highest = df.loc[df["Marks"].idxmax()]
        lowest = df.loc[df["Marks"].idxmin()]

        report.append("\n4. STUDENT PERFORMANCE")
        report.append(
            f"Highest Scorer: {highest['Name']} - {highest['Marks']}"
        )
        report.append(
            f"Lowest Scorer: {lowest['Name']} - {lowest['Marks']}"
        )

    # 5. Department analysis
    if "Department" in df.columns and "Marks" in df.columns:

        department_avg = df.groupby("Department")["Marks"].mean()

        report.append("\n5. DEPARTMENT PERFORMANCE")

        for department, average in department_avg.items():
            report.append(f"{department}: {average:.2f}")

    # Save report
    report_text = "\n".join(report)

    with open("reports/analysis_report.txt", "w", encoding="utf-8") as file:
        file.write(report_text)

    print(report_text)

    print("\nReport saved successfully!")
    print("Location: reports/analysis_report.txt")

    print("\n========== REPORT COMPLETED ==========")
