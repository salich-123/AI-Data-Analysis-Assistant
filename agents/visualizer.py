
import matplotlib.pyplot as plt

def create_visualizations(df):

    print("\n========== CREATING CHARTS ==========")

    # 1. Department-wise average marks
    department_marks = df.groupby("Department")["Marks"].mean()

    plt.figure(figsize=(8, 5))

    department_marks.plot(kind="bar")

    plt.title("Average Marks by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Marks")

    plt.tight_layout()

    plt.savefig("reports/department_marks.png")

    plt.show()

    # 2. Student marks comparison
    plt.figure(figsize=(8, 5))

    plt.bar(df["Name"], df["Marks"])

    plt.title("Student Marks Comparison")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")

    plt.tight_layout()

    plt.savefig("reports/student_marks.png")

    plt.show()

    print("\nCharts saved successfully!")
    print("Check the reports folder.")

    print("\n========== VISUALIZATION COMPLETED ==========")
