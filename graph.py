import matplotlib.pyplot as plt

def create_graph(students):
    
    student_data = []
    
    for student in students:
        student_data.append(student.ranking_data.high_low)

    # Create a boxplot
    fig, ax = plt.subplots()
    ax.boxplot(student_data)

    # Set the title and labels
    ax.set_title('Student Performance')
    ax.set_xlabel('Students')
    ax.set_ylabel('Ranking')

    # Show the plot
    plt.show()
