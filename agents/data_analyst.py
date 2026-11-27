def analyze_data(df):

    print("\n========== DATA ANALYSIS ==========")

    # 1. Select numerical columns
    numerical_data = df.select_dtypes(include="number")

    # 2. Calculate average values
    print("\n1. Average Values:")
    print(numerical_data.mean())

    # 3. Find maximum values
    print("\n2. Maximum Values:")
    print(numerical_data.max())

    # 4. Find minimum values
    print("\n3. Minimum Values:")
    print(numerical_data.min())

    # 5. Find highest and lowest marks
    if "Marks" in df.columns:

        highest_student = df.loc[df["Marks"].idxmax()]

        lowest_student = df.loc[df["Marks"].idxmin()]

        print("\n4. Highest Marks:")
        print(highest_student[["Name", "Marks"]])

        print("\n5. Lowest Marks:")
        print(lowest_student[["Name", "Marks"]])

    # 6. Department-wise average marks
    if "Department" in df.columns and "Marks" in df.columns:

        print("\n6. Department-wise Average Marks:")

        department_average = df.groupby("Department")["Marks"].mean()

        print(department_average)

    print("\n========== ANALYSIS COMPLETED ==========")
