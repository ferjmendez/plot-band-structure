#Import packages and graph configuration
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Insert here a system label. You could create a directory called "syslabel"

#Example for FeSe P4/nmm band structure and DOS by DFT calculations
syslabel="FeSe"
#File directory (path). Select a work directory with your information and files
path=f"C:/Users/Computo/Documents/fatbands_DOS/{syslabel}"
#Bands file
bands_file=f"{path}/bands_{syslabel}.dat.gnu"
#Ticks file
ticks_file=f"{path}/HS-points.txt"
#3d orbitals file
orbital_3d_file=f"{path}/{syslabel}_Fe_3d.dat"
#DOS file
dos_file=f"{path}/dos.dat"

#Graph's format for matplotlib
import matplotlib
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica"],
        "text.usetex": True,
        "pgf.rcfonts": False,
        "axes.unicode_minus": False,
        "font.size": 12,
        "figure.dpi": 600,
        "pgf.preamble": "\n".join([ 
	# Next packages be required to insert characters like "Gamma" or another greek or math symbols
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{amsmath}",
        r"\usepackage{amsfonts}",
        r"\usepackage[spanish]{babel}",
        r"\usepackage{amssymb}",
        ])
    }
)

#Open and read ticks file with a function
def read_ticks(filename):
    #Read with pandas 
    df_ticks=pd.read_csv(filename, sep='\s+')
    #Fix "ticks file" to format required
    df_ticks.columns=["High-symmetry point", "position"]
    return df_ticks
    
ticks=read_ticks(ticks_file)
#Convert to list makes easier work with strings like high-symmetry point names
labels=ticks["High-symmetry point"].tolist()
pos=ticks["position"].tolist()
ticks_lines=[]
for i in range(len(labels)):
        #Greek label for Gamma high-symmetry point
        if labels[i]=="Gamma":
            ticks_lines.append((r"$\Gamma$", float(pos[i])))
        else:
            ticks_lines.append((labels[i], float(pos[i])))

#Set Fermi Level value to your system
fermi_level=11.9067 #eV 

#Open and read bands file
def read_bands(filename):
    df_bands=pd.read_csv(filename,sep='\s+',header=None)
    df_bands.columns=["k","E"]
    #If your energy values have been set at EF = 0 you can comment next line
    df_bands["E-EF"]=df_bands["E"]-fermi_level
    return df_bands
bands=read_bands(bands_file)    

#Tracked bands for smooth graph using lines. "Groupby" is a excelent tool
grouped = bands.groupby("k")
k_vals = []
bands_raw = []

for k, group in grouped:
    k_vals.append(k)
    bands_raw.append(group["E-EF"].values)

#Order k-points and energy to identify different bands
min_bands = min(len(b) for b in bands_raw)
bands_raw = [np.sort(b)[:min_bands] for b in bands_raw]

tracked = []
tracked.append(np.sort(bands_raw[0]))  # First k ordered

#Order the missing ones
for i in range(1, len(bands_raw)):
    prev = tracked[-1]
    current = bands_raw[i]

    assigned = []
    remaining = list(current)

    for e_prev in prev:
        # Found nearest point (k, E(k))
        idx = np.argmin([abs(e_prev - e) for e in remaining])
        assigned.append(remaining.pop(idx))

    tracked.append(np.array(assigned))

#New lists with tracked bands
tracked = np.array(tracked)
k_vals = np.array(k_vals)

#Open and read fatbands

#An example for d-orbitals
def read_weight(filename):
    #Read data file with pandas
    df_weight=pd.read_csv(filename,sep='\s+',comment='#',header=None)
    #Rename columns to identify orbital components
    df_weight.columns=["k index", "k","E-EF","Total","dz2","dzx","dzy","dx2-y2","dxy"]
    return df_weight
    
orb_3d=read_weight(orbital_3d_file)
#Normalize dzx-orbital weights
weight_d=orb_3d["dzx"]/orb_3d["dzx"].max()

#Open and read DOS/PDOS files

def read_DOS(filename):
    df_dos=pd.read_csv(filename, sep='\s+', comment='#', header=None)
    df_dos.columns=["E","DOS", "INT DOS"]
    # Only if Fermi level isn't fix at zero 
    df_dos["E-EF"]=df_dos["E"]-fermi_level
    return df_dos
    
dos=read_DOS(dos_file)

#Function to plot graphs with minimal parameters. Fix titlename, xlim, ylim and filename to save plot.
#Alpha is the circle transparence for spectral weight of orbitals
def plot_fatbands_DOS(weight_scale,title=None, xlim=None, ylim=None,alpha=None,graph_file=None):
    #Present band structure and PDOS projected in left hand and DOS/PDOS in right hand
    fig, (ax_bands, ax_dos) = plt.subplots(
    1, 2,
    #Image size to save
    figsize=(10, 6),
    #Ratio aspect. 3 is for bands: 1 is for DOS. You can change it
    gridspec_kw={'width_ratios': [3, 1]}  )

#Left hand plot
    ax_bands.scatter(orb_3d["k"], orb_3d["E-EF"], s=weight_d*weight_scale, label=r"$d_{xz}$ orbitals", color='red', alpha=alpha)
    #Show orbital label in plot
    ax_bands.legend()

    #Add tracked bands to plot
    for i in range(tracked.shape[1]):
        ax_bands.plot(k_vals, tracked[:, i], color='black', lw=0.5)

    #Add vertical lines at high symmetry points and ticks (and their labels)
    for label, pos in ticks_lines:
        ax_bands.axvline(x=pos, color='black', lw=0.5)
    ax_bands.set_xticks([pos for _, pos in ticks_lines], [lbl for lbl, _ in ticks_lines])

#Right hand plot    
    ax_dos.plot(dos["DOS"],dos["E-EF"],color='black',lw=0.5,label=r"Total DOS")
    ax_dos.legend()
    
    # Axes labels and limits
    ax_bands.set_xlim(xlim)
    ax_dos.set_xlim(0,1.1*dos["DOS"].max())
    ax_dos.set_xlabel(r"$DOS (arb.units)$")
    ax_bands.set_ylim(ylim)
    ax_dos.set_ylim(ylim)
    ax_dos.sharey(ax_bands)
    ax_bands.grid(False)
    ax_dos.grid(False)

    # Optional: Remove the identical labels
    ax_bands.set_ylabel(r"$E-E_F (eV)$")
    ax_bands.set_yticklabels([])
    plt.subplots_adjust(wspace=0.05)
    plt.title(title)

    # Optional: zero energy line at Fermi level
    ax_bands.axhline(y=0, color='black', linestyle='--', lw=0.5)

    plt.tight_layout()
    #Save graph in an image file
    plt.savefig(graph_file)
    plt.show()

#Complete band structure and DOS
graph_file=f"{path}/fatbands_dos_{syslabel}.png"
#Edit with your info
weight_scale=100
alpha=0.1
xlim=(0,max(pos))
ylim=(-2, 2)
plot_fatbands_DOS(weight_scale,title=None, xlim=xlim, ylim=ylim,alpha=alpha,graph_file=graph_file)