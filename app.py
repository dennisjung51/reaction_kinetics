from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import numpy as np
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    k1 = float(data['k1'])
    k2 = float(data['k2'])

    N = 100  # Time range
    A = 100  # Initial concentration

    x = np.linspace(0, N, num=400)

    if abs(k1 - k2) < 1e-9:
        k2 += 1e-9

    y_A = A * np.exp(-k1 * x)
    y_B = (k1 * A * (np.exp(-k1 * x) - np.exp(-k2 * x))) / (k2 - k1)
    y_C = A * (1 + (k1 * np.exp(-k2 * x) - k2 * np.exp(-k1 * x)) / (k2 - k1))

    # Convert numpy arrays to lists for JSON serialization
    x_list = x.tolist()
    y_A_list = y_A.tolist()
    y_B_list = y_B.tolist()
    y_C_list = y_C.tolist()

    # Create Plotly figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_list, y=y_A_list, 
        mode='lines', 
        name='A (Reactant)',
        line=dict(color='#2E7D32', width=2.5),
        hovertemplate='<b>Species A</b><br>Time: %{x:.1f} min<br>Concentration: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=x_list, y=y_B_list, 
        mode='lines', 
        name='B (Intermediate)',
        line=dict(color='#1565C0', width=2.5),
        hovertemplate='<b>Species B</b><br>Time: %{x:.1f} min<br>Concentration: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=x_list, y=y_C_list, 
        mode='lines', 
        name='C (Product)',
        line=dict(color='#C62828', width=2.5),
        hovertemplate='<b>Species C</b><br>Time: %{x:.1f} min<br>Concentration: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='<b>Reaction time</b> / min',
        yaxis_title='<b>Concentration</b> / %',
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridwidth=1,
            gridcolor='#E8E8E8',
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor='#BDBDBD',
            showline=True,
            linewidth=1.5,
            linecolor='#424242',
            mirror=True
        ),
        yaxis=dict(
            range=[0, 101],
            showgrid=True,
            gridwidth=1,
            gridcolor='#E8E8E8',
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor='#BDBDBD',
            showline=True,
            linewidth=1.5,
            linecolor='#424242',
            mirror=True
        ),
        height=520,
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        margin=dict(l=70, r=40, t=40, b=60),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'
        ),
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#BDBDBD',
            borderwidth=1,
            font=dict(size=12)
        ),
        font=dict(
            family='Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size=13,
            color='#212121'
        )
    )
    
    # Return Plotly JSON for client-side rendering
    return jsonify(fig.to_dict())

if __name__ == '__main__':
    # Check if running on Railway (PORT env variable is set)
    if 'PORT' in os.environ:
        port = int(os.environ.get('PORT', 5000))
        print(f'Starting Flask app on 0.0.0.0:{port} (Production mode)')
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print('Starting Flask app in local development mode on http://127.0.0.1:5000')
        app.run(debug=True)

