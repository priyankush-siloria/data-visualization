import matplotlib.pyplot as plt
import csv
import json
import ast

data = {}
with open('ViatorTags.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['parentTagIds']:
            all_names = json.loads(row['allNamesByLocale'].replace("''", '"'))
            parent_tags = ast.literal_eval(row['parentTagIds'])
            en_name = all_names.get('en', '')

            for parent_tag in parent_tags:
                data.setdefault(parent_tag, []).append({row['tagId']: en_name})


class Node:
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children
        self.visible = False

def toggle_children(event):
    ax = plt.gca()
    plt.cla()
    plt.axis('off')
    
    parent = event.artist.get_label()
    children_texts = [t for t in ax.texts if t.get_text() == parent]
    
    if children_texts:
        y_pos = children_texts[0].get_position()[1]
        for t in ax.texts:
            if t.get_position()[1] < y_pos:
                t.set_visible(not t.get_visible())
                
    draw_tree(ax, data, 0.1, 0.8)
    plt.draw()

def draw_tree(ax, data, x, y):
    y_start = y
    nodes = []
    for parent, children in data.items():
        node = Node(parent, children)
        nodes.append(node)
        
        # Add a small button next to parent
        bbox_props = dict(boxstyle="circle,pad=0.3", fc="cyan", ec="b", lw=2)
        ax.text(x - 0.05, y, '+', va='center', ha='center', fontsize=12, bbox=bbox_props, picker=True)
        ax.text(x, y, f"{parent}", va='center', ha='left', fontsize=12, fontweight='bold', color='blue')
        y -= 0.1
        for child in children:
            key, value = list(child.items())[0]
            plt.text(x + 0.05, y, f"{key} - {value}", va='center', ha='left', fontsize=10)
            y -= 0.1
        y -= 0.2

    fig = plt.gcf()
    fig.canvas.mpl_connect('pick_event', toggle_children)

plt.figure(figsize=(15, 10))
plt.axis('off')
ax = plt.gca()

draw_tree(ax, data, 0.1, 0.8)

plt.title('Hierarchical Visualization of Categories', fontsize=16)
plt.tight_layout()
plt.show()
