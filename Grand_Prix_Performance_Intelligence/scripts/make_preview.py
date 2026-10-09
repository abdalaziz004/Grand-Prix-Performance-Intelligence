"""Create a static portfolio preview image from the reproducible CSV outputs.
The file is intentionally labelled as a static analysis preview, not a Power BI screenshot.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
ASSETS=ROOT/'assets'; ASSETS.mkdir(exist_ok=True)
summary=pd.read_json(OUT/'quality_summary.json', typ='series')
constructors=pd.read_csv(OUT/'constructor_win_leaderboard.csv').head(5)
yearly=pd.read_csv(OUT/'yearly_summary.csv')
drivers=pd.read_csv(OUT/'driver_win_leaderboard.csv').head(3)
shares=pd.read_csv(OUT/'constructor_win_share_by_season.csv')
redbull2023=shares[(shares['Year']==2023)&(shares['Constructor']=='Red Bull')].iloc[0]

NAVY='#0B1220'; PANEL='#111C2F'; PANEL2='#17253B'; WHITE='#F2F6FC'; MUTED='#9FB0C5'; CYAN='#45D6C5'; BLUE='#5EA8FF'; AMBER='#FFB86B'; RED='#FF7A90'; GRID='#253750'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':WHITE,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED})
fig=plt.figure(figsize=(16,9), dpi=120, facecolor=NAVY)
fig.text(0.045,0.93,'GRAND PRIX PERFORMANCE INTELLIGENCE',fontsize=23,fontweight='bold',color=WHITE)
fig.text(0.046,0.895,'FORMULA 1  ·  SPORTS & MEDIA ANALYTICS  ·  F1DB SNAPSHOT v2026.8.2',fontsize=10,color=MUTED)
fig.text(0.956,0.928,'PORTFOLIO PREVIEW',fontsize=9,fontweight='bold',color=CYAN,ha='right')
fig.text(0.956,0.897,'Static CSV analysis · not a Power BI screenshot',fontsize=8,color=MUTED,ha='right')

# KPI cards
kpis=[
 ('RACE-RESULT ROWS',f"{int(summary['race_result_rows']):,}",'source result records',CYAN),
 ('RACES WITH RESULTS',f"{int(summary['distinct_race_events_with_result_rows']):,}",'distinct race IDs',BLUE),
 ('BLANK FINISH POSITION',f"{summary['blank_position_rate_pct']:.2f}%",'not equivalent to DNF',AMBER),
 ('RED BULL · 2023',f"{redbull2023['WinSharePct']:.2f}%",f"{int(redbull2023['RaceWins'])} wins of {int(redbull2023['EventsWithResult'])} events",CYAN),
]
xs=[0.045,0.277,0.509,0.741]
for x,(label,value,sub,accent) in zip(xs,kpis):
    ax=fig.add_axes([x,0.745,0.214,0.115]); ax.set_axis_off()
    card=FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.015,rounding_size=0.035',facecolor=PANEL,edgecolor=GRID,linewidth=1.0,transform=ax.transAxes,clip_on=False)
    ax.add_patch(card); ax.add_patch(FancyBboxPatch((0.03,0.14),0.012,0.72,boxstyle='round,pad=0.002,rounding_size=0.005',facecolor=accent,edgecolor=accent,transform=ax.transAxes))
    ax.text(0.09,0.74,label,fontsize=8.2,color=MUTED,fontweight='bold',transform=ax.transAxes)
    ax.text(0.09,0.39,value,fontsize=21,color=WHITE,fontweight='bold',transform=ax.transAxes)
    ax.text(0.09,0.14,sub,fontsize=8.0,color=accent,transform=ax.transAxes)

# Left chart: top constructors
ax=fig.add_axes([0.055,0.31,0.42,0.36],facecolor=PANEL)
for s in ax.spines.values(): s.set_visible(False)
ax.grid(axis='x',color=GRID,linewidth=0.8)
ax.set_axisbelow(True)
bar_values=constructors['RaceWins'].values[::-1]
bar_labels=constructors['name'].values[::-1]
bars=ax.barh(bar_labels,bar_values,color=[CYAN if i==len(bar_values)-1 else BLUE for i in range(len(bar_values))],height=0.55)
ax.tick_params(axis='both',length=0,labelsize=9)
ax.set_xlabel('Distinct race events with a winning result',fontsize=8,labelpad=8)
ax.set_title('CONSTRUCTOR WINS · ALL YEARS IN SNAPSHOT',loc='left',fontsize=10,fontweight='bold',pad=14,color=WHITE)
ax.set_xlim(0,max(bar_values)*1.17)
for b,v in zip(bars,bar_values):
    ax.text(v+2,b.get_y()+b.get_height()/2,f'{int(v)}',va='center',fontsize=9,color=WHITE,fontweight='bold')

# Right chart: explicit DNF trend
ax2=fig.add_axes([0.535,0.31,0.41,0.36],facecolor=PANEL)
for s in ax2.spines.values(): s.set_visible(False)
ax2.grid(axis='y',color=GRID,linewidth=0.8); ax2.set_axisbelow(True)
y=yearly.dropna(subset=['ExplicitDNFRatePct']).copy()
y=y[y['Year']>=1950]
# A five-year rolling mean smooths year-to-year volatility; rates remain visible by year.
y['Smooth5']=y['ExplicitDNFRatePct'].rolling(5,min_periods=2).mean()
ax2.fill_between(y['Year'].astype(float),y['Smooth5'].astype(float),alpha=0.12,color=CYAN)
ax2.plot(y['Year'],y['Smooth5'],color=CYAN,linewidth=2.5)
ax2.plot(y['Year'],y['ExplicitDNFRatePct'],color=BLUE,linewidth=0.8,alpha=0.38)
ax2.axvline(2025,color=AMBER,linestyle='--',linewidth=1.1,alpha=0.8)
ax2.text(2025.3, max(y['ExplicitDNFRatePct'].max(),50)*0.90,'2026 partial',fontsize=7.5,color=AMBER,rotation=90,va='top')
ax2.set_xlim(1950,2027); ax2.set_ylim(0,max(75,y['ExplicitDNFRatePct'].max()+5))
ax2.tick_params(axis='both',length=0,labelsize=8)
ax2.set_xlabel('Season year',fontsize=8,labelpad=8); ax2.set_ylabel('Explicit DNF rows / result rows (%)',fontsize=8,labelpad=8)
ax2.set_title('EXPLICIT DNF RATE · FIVE-YEAR SMOOTH',loc='left',fontsize=10,fontweight='bold',pad=14,color=WHITE)

# Bottom findings strip
ax3=fig.add_axes([0.045,0.105,0.91,0.135]); ax3.set_axis_off()
rect=FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.012,rounding_size=0.03',facecolor=PANEL2,edgecolor=GRID,linewidth=1.0,transform=ax3.transAxes)
ax3.add_patch(rect)
ax3.text(0.025,0.75,'THREE FINDINGS THAT CHANGE HOW THE REPORT SHOULD BE READ',fontsize=8.5,color=CYAN,fontweight='bold',transform=ax3.transAxes)
findings=[
    ('106','Lewis Hamilton · distinct race wins'),
    ('31.88%','explicit DNF labels (not blank-position rate)'),
    ('1994+','pit-stop timing coverage in this snapshot'),
]
for i,(big,small) in enumerate(findings):
    x=0.025+i*0.32
    ax3.text(x,0.39,big,fontsize=18,color=WHITE,fontweight='bold',transform=ax3.transAxes)
    ax3.text(x,0.14,small,fontsize=8.4,color=MUTED,transform=ax3.transAxes)

fig.text(0.046,0.055,'Source: F1DB · CC BY 4.0 · https://github.com/f1db/f1db',fontsize=8.2,color=MUTED)
fig.text(0.955,0.055,'2026 results populated through Round 8 in this frozen extract',fontsize=8.2,color=AMBER,ha='right')
fig.savefig(ASSETS/'dashboard_preview.png',dpi=120,facecolor=NAVY,bbox_inches='tight')
plt.close(fig)
print(f'created {ASSETS / "dashboard_preview.png"}')
