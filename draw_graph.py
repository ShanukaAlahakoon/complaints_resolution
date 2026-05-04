from graph import build_graph
from IPython.display import Image, display
from PIL import Image as PILImage
import io

# Build the graph
app = build_graph()

# Draw the graph as PNG
png_data = app.get_graph().draw_mermaid_png()

# Save to file
with open("agent_graph.png", "wb") as f:
    f.write(png_data)

print("Graph saved as agent_graph.png ✅")

# Show the image
image = PILImage.open(io.BytesIO(png_data))
image.show()