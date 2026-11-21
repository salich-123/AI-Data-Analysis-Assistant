
def answer_question(df, question):

    question = question.lower().strip()

    question_words = (
        question.replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .split()
    )

    # 1. Total records
    if any(phrase in question for phrase in [
        "total records",
        "number of records",
        "how many records",
        "total number of records",
        "how many rows"
    ]):
        return f"Total records: {len(df)}"

    # 2. Missing values
    elif "missing values" in question or "null values" in question:
        total = int(df.isnull().sum().sum())
        return f"Total missing values: {total}"

    # 3. Correlation analysis
    elif "correlation" in question_words:

        numerical_columns = df.select_dtypes(include="number").columns

        selected_columns = []

        for column in numerical_columns:
            if str(column).lower() in question_words:
                selected_columns.append(column)

        if len(selected_columns) == 2:

            correlation = df[selected_columns[0]].corr(
                df[selected_columns[1]]
            )

            return (
                f"Correlation between {selected_columns[0]} and "
                f"{selected_columns[1]}: {correlation:.2f}"
            )

        return "Please mention two numerical column names."

    # 4. Department-wise average marks
    elif "department" in question_words and "average" in question_words:

        if "Department" in df.columns and "Marks" in df.columns:

            result = df.groupby("Department")["Marks"].mean()

            return "Department-wise average marks:\n" + result.to_string()

        return "Department or Marks column not found."

    # 5. Students by department
    elif "department" in question_words and any(
        word in question_words for word in ["show", "list", "display", "which"]
    ):

        if "Department" in df.columns:

            for department in df["Department"].dropna().unique():

                if str(department).lower() in question:

                    result = df[df["Department"] == department]

                    return (
                        f"Students in {department} department:\n"
                        + result.to_string(index=False)
                    )

            return "Department not found in the dataset."

        return "Department column not found."

    # 6. Department-wise student count
    elif "department" in question_words and any(
        word in question_words for word in ["count", "number", "students"]
    ):

        if "Department" in df.columns:

            result = df["Department"].value_counts()

            return "Department-wise student count:\n" + result.to_string()

        return "Department column not found."

    # 7. Search student details by name
    elif any(word in question_words for word in [
        "details", "information", "profile", "search"
    ]):

        if "Name" in df.columns:

            for name in df["Name"].dropna().unique():

                if str(name).lower() in question:

                    result = df[df["Name"] == name]

                    return (
                        "Student details:\n"
                        + result.to_string(index=False)
                    )

            return "Student not found in the dataset."

        return "Name column not found."

    # 8. Top N student analysis
    elif "top" in question_words and any(
        word in question_words for word in ["marks", "salary"]
    ):

        numbers = [
            int(word) for word in question_words if word.isdigit()
        ]

        if not numbers:
            return "Please mention how many students to display."

        count = numbers[0]

        column = "Marks" if "marks" in question_words else "Salary"

        if column not in df.columns:
            return f"{column} column not found."

        result = df.sort_values(
            by=column,
            ascending=False
        ).head(count)

        return (
            f"Top {count} students by {column}:\n"
            + result.to_string(index=False)
        )

    # 9. Sort students by marks
    elif "marks" in question_words and any(
        word in question_words for word in [
            "sort", "sorted", "rank", "arrange", "order", "ranking"
        ]
    ):

        if "Marks" in df.columns:

            descending = any(word in question_words for word in [
                "highest", "descending", "top", "rank", "ranking"
            ])

            result = df.sort_values(
                by="Marks",
                ascending=not descending
            )

            return "Students sorted by marks:\n" + result.to_string(index=False)

        return "Marks column not found."

    # 10. Filter students by marks range
    elif "marks" in question_words and "between" in question_words:

        if "Marks" in df.columns:

            numbers = [
                int(word) for word in question_words if word.isdigit()
            ]

            if len(numbers) < 2:
                return "Please provide two marks values."

            lower_limit = numbers[0]
            upper_limit = numbers[1]

            result = df[
                (df["Marks"] >= lower_limit) &
                (df["Marks"] <= upper_limit)
            ]

            if result.empty:
                return "No students found in this marks range."

            return "Students within marks range:\n" + result.to_string(index=False)

        return "Marks column not found."

    # 11. Filter students by marks
    elif "marks" in question_words and any(
        word in question_words for word in [
            "above", "below", "greater", "less"
        ]
    ):

        if "Marks" in df.columns:

            numbers = [
                int(word) for word in question_words if word.isdigit()
            ]

            if not numbers:
                return "Please mention a marks value."

            threshold = numbers[0]

            if any(word in question_words for word in ["above", "greater"]):
                result = df[df["Marks"] > threshold]
            else:
                result = df[df["Marks"] < threshold]

            if result.empty:
                return "No students found for this condition."

            return "Filtered student records:\n" + result.to_string(index=False)

        return "Marks column not found."

    # 12. Filter students by salary
    elif "salary" in question_words and any(
        word in question_words for word in [
            "above", "below", "greater", "less"
        ]
    ):

        if "Salary" in df.columns:

            numbers = [
                int(word) for word in question_words if word.isdigit()
            ]

            if not numbers:
                return "Please mention a salary value."

            threshold = numbers[0]

            if any(word in question_words for word in ["above", "greater"]):
                result = df[df["Salary"] > threshold]
            else:
                result = df[df["Salary"] < threshold]

            if result.empty:
                return "No students found for this condition."

            return "Filtered student records:\n" + result.to_string(index=False)

        return "Salary column not found."

    # 13. Median and standard deviation
    elif any(word in question_words for word in [
        "median", "standard", "deviation"
    ]):

        for column in df.select_dtypes(include="number").columns:

            if str(column).lower() in question_words:

                if "median" in question_words:
                    return f"Median {column}: {df[column].median():.2f}"

                elif "standard" in question_words or "deviation" in question_words:
                    return f"Standard deviation of {column}: {df[column].std():.2f}"

        return "Please mention a valid numerical column."

    # 14. General numerical analysis
    numerical_columns = df.select_dtypes(include="number").columns

    for column in numerical_columns:

        column_name = str(column).lower()

        if column_name in question_words:

            # Average
            if "average" in question_words or "mean" in question_words:

                average = df[column].mean()

                return f"Average {column}: {average:.2f}"

            # Highest value
            elif any(word in question_words for word in [
                "highest", "maximum", "max"
            ]):

                highest_index = df[column].idxmax()
                highest_value = df.loc[highest_index, column]

                if "Name" in df.columns:
                    student_name = df.loc[highest_index, "Name"]
                    return f"{student_name} has the highest {column}: {highest_value}"

                return f"Highest {column}: {highest_value}"

            # Lowest value
            elif any(word in question_words for word in [
                "lowest", "minimum", "min"
            ]):

                lowest_index = df[column].idxmin()
                lowest_value = df.loc[lowest_index, column]

                if "Name" in df.columns:
                    student_name = df.loc[lowest_index, "Name"]
                    return f"{student_name} has the lowest {column}: {lowest_value}"

                return f"Lowest {column}: {lowest_value}"

    return "Sorry, I cannot answer this question yet."
