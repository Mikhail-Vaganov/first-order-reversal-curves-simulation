# First order reversal curve (FORC) diagrams simulation

The FORC diagrams analysis is implemented by the FORC processors, for instance, by the PikeFORC class.
FORC analysis can be applied to a Magnetic matter simulating object which implements. 
For example, in order to simulate a single particle model use an instance of the SingleParticleMatter class, whose constructor takes in turn a MagneticParticle object.

```python
h = Hysteron(2.0, -2.0)
matter = SingleParticleMatter(h)
forc = PikeFORC(3, -1, 1, matter, output_directory)
forc.magnetization_forc()
forc.calculate_forc_distribution()
forc.draw_forc_diagram_hc_hu()
```

## Stoner-Wohlfarth model simulation

```python
p = SwParticle(np.pi/3)
p.draw(output_directory)
```

## References
1. Pike, Roberts, Verosub, JAP 1999
2. [Vaganov, Linke, Odenbach, Raikher, JMMM 2015](http://www.sciencedirect.com/science/article/pii/S0304885316319552)