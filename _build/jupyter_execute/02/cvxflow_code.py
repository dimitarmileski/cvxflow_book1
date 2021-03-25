# CVXFlow

import numpy as np
import gropt
import scipy.io as sio
import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from IPython.core.display import display, HTML
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}
 

n_it = 2000  # Number of iterations for optimizer
smax = 200.0  # Slew rate in T/m/s
tmax = 0.7  # PNS threshold
gmax = 80.0 # Gradient max in mT/m
cushion = 1.0  # This will derate gmax, smax and tmax if needed

r_venc = 120.0  # Venc (cm/s)
r_res = np.array([-1.5, 1.5, 1.5])  # Resolution (mm)

E = np.array([[-1, 1, -1],
                  [-1, 1, 1],
                  [-1, -1, -1],
                  [1, 1, -1]])

r_m0 = 11.74 * 1.0 / r_res  # Convert to units M0
r_init_m1 = 7.33 * 80.0 / r_venc  # convert to M1



dt = 40e-3  # 40 us solve raster
N = 32 # How long the gradient is"


line_c = -1.0  # K-space line in ky, scaled to -1.0 to 1.0
par_c = -1.0  # K-space line in kz, scaled to -1.0 to 1.0

d_M0 = r_m0 * [1.0, line_c, par_c]


m1_shift = np.array([-5.28,4.16*line_c,4.56*par_c])
i = 0
d_M1 = E[i] * r_init_m1 + m1_shift


G, resid = gropt.opt3(N, d_M0, d_M1, dt=dt, n_it = n_it, cushion = cushion, gmax = gmax, smax = smax, tmax = tmax)
print(resid)

G3_old = np.reshape(G, (3,-1))
x = np.arange(29)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=G3_old[0],
                    mode='lines',
                    line=dict(color='rgb(88, 153, 199)'),
                    name = 'Gx'
                    ))
fig.add_trace(go.Scatter(x=x, y=G3_old[1],
                    mode='lines',
                    line=dict(color='rgb(255, 147, 52)'),
                    name = 'Gy'
                         
                    ))
fig.add_trace(go.Scatter(x=x, y=G3_old[2],
                    mode='lines',
                    line = dict(color = 'rgb(105, 187, 105)'),
                    name = 'Gz'
                     ))

fig.update_layout(xaxis_title="time (ms)", yaxis_title="Gradient (mT/m)")
#Binder and ThebeLab
plot(fig, filename = 'fig.html', config = config)

#ThebeLab
display(HTML('fig.html'))
#Binder
#plot(fig,config=config)

# Repeat with no pns
tmax = 100.0
N = 29 # Shorter

i = 0
d_M1 = E[i] * r_init_m1 + m1_shift


G, resid = gropt.opt3(N, d_M0, d_M1, dt=dt, n_it = n_it, cushion = cushion, gmax = gmax, smax = smax, tmax = tmax)
print(resid)

G3 = np.reshape(G, (3,-1))
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=G3[0],
                    mode='lines',
                    line=dict(color='rgb(88, 153, 199)'),
                    name = 'Gx'
                    ))
fig2.add_trace(go.Scatter(x=x, y=G3[1],
                    mode='lines',
                    line=dict(color='rgb(255, 147, 52)'),
                    name = 'Gy'
                    ))
fig2.add_trace(go.Scatter(x=x, y=G3[2],
                    mode='lines',
                    line = dict(color = 'rgb(105, 187, 105)'),
                    name = 'Gz'
                     ))

fig2.update_layout(xaxis_title="time (ms)",  yaxis_title="Gradient (mT/m)")
#Binder and ThebeLab
plot(fig2, filename = 'fig2.html', config = config)

#ThebeLab
display(HTML('fig2.html'))
#Binder
#plot(fig2,config=config)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=x, y=G3_old[0],
                    mode='lines',
                    name = 'Gx before',
                    line=dict(color='rgb(88, 153, 199)')
                    ))
fig3.add_trace(go.Scatter(x=x, y=G3[0],
                    mode='lines',
                    name = 'Gx after'
                    ))
fig3.add_trace(go.Scatter(x=x, y=G3_old[1],
                    mode='lines',
                     name = 'Gy before',
                     visible = False,
                     line=dict(color='rgb(255, 147, 52)')
                    ))
fig3.add_trace(go.Scatter(x=x, y=G3[1],
                    mode='lines',
                    visible = False,
                    name = 'Gy after'
                    ))
fig3.add_trace(go.Scatter(x=x, y=G3_old[2],
                    mode='lines',
                    visible = False,      
                    name = 'Gz before',
                    line = dict(color = 'rgb(105, 187, 105)')
                     ))
fig3.add_trace(go.Scatter(x=x, y=G3[2],
                    mode='lines',
                    name = 'Gz after',
                    visible = False,
                    
                     ))

fig3.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Gx",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False]},
                           {"title": "Line 1 comparation"}]),
                dict(label="Gy",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False]},
                           {"title": "Line 2 comparation"
                            }]),
                dict(label="Gz",
                     method="update",
                     args=[{"visible": [False, False,False,False, True, True]},
                           {"title": "Line 3 comparation"}]),
               
            ]),
        )
    ])
fig3.update_layout(title_text="Before and After Comparation")

fig3.update_layout(xaxis_title="time (ms)", yaxis_title="Gradient (mT/m)")


#Binder and ThebeLab
plot(fig3, filename = 'fig3.html', config = config)

#ThebeLab
display(HTML('fig3.html'))
#Binder
# iplot(fig3,config=config)

