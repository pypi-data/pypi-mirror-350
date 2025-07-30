import marimo as mo
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib import axes, figure
from matplotlib.ticker import MaxNLocator
from weas_widget import WeasWidget

from .cube import Cube
from .output import AimsOutput


class VisualiseAims(AimsOutput):
    """
    FHI-aims visualisation tools.

    ...

    Attributes
    ----------
    scf_conv_acc_params : dict
        the SCF convergence accuracy parameters
    """

    @staticmethod
    def _plot_charge_convergence(
        ax: axes.Axes,
        tot_scf_iters: npt.NDArray[np.int64] | list[int],
        delta_charge: npt.NDArray[np.float64] | list[float],
        delta_charge_sd: npt.NDArray[np.float64] | list[float] | None = None,
        conv_params: dict | None = None,
        title: str | None = None,
    ) -> axes.Axes:
        """
        Create a subplot for the charge convergence of an FHI-aims calculation.

        Parameters
        ----------
        ax : axes.Axes
            matplotlib subplot index
        tot_scf_iters : npt.NDArray[np.int64] | list[int]
            cumulative SCF iterations
        delta_charge : npt.NDArray[np.float64] | list[float]
            change of spin-up or total spin (if the calculation was spin none)
            eigenvalues
        delta_charge_sd : npt.NDArray[np.float64] | list[float] | None, default=None
            change of spin-down eigenvalues
        conv_params : dict | None, default=None
            convergence parameters which determine if the SCF cycle has converged
        title : str | None, default=None
            system name to include in title

        Returns
        -------
        axes.Axes
            matplotlib subplot object
        """
        ax.plot(tot_scf_iters, delta_charge, label=r"$\Delta$ charge")

        # Only plot delta_charge_sd if the calculation is spin polarised
        if delta_charge_sd is not None:
            ax.plot(
                tot_scf_iters, delta_charge_sd, label=r"$\Delta$ charge/spin density"
            )

        # Add the convergence parameters
        if conv_params is not None and conv_params["charge_density"] != 0.0:
            ax.axhline(
                conv_params["charge_density"],
                ls="--",
                c="gray",
                label=r"$\rho$ convergence criterion",
            )

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_yscale("log")
        ax.set_xlabel("cumulative SCF iteration")
        ax.set_ylabel(r"Charge / $e a_0^{-3}$")
        ax.legend()
        if title is not None:
            ax.set_title(rf"{title} $\Delta$ charge Convergence")

        return ax

    @staticmethod
    def _plot_energy_convergence(
        ax: axes.Axes,
        tot_scf_iters: npt.NDArray[np.int64] | list[int],
        delta_sum_eigenvalues: npt.NDArray[np.float64] | list[float],
        delta_total_energies: npt.NDArray[np.float64] | list[float],
        conv_params: dict | None = None,
        absolute: bool = True,
        title: str | None = None,
    ) -> axes.Axes:
        """
        Create a subplot for the energy convergence of an FHI-aims calculation.

        Parameters
        ----------
        ax : axes.Axes
            matplotlib subplot index
        tot_scf_iters : npt.NDArray[np.int64] | list[int]
            cumulative SCF iterations
        delta_sum_eigenvalues : npt.NDArray[np.float64] | list[float]
            change of sum of eigenvalues
        delta_total_energies : npt.NDArray[np.float64] | list[float]
            change of total energies
        conv_params : dict | None, default=None
            convergence parameters which determine if the SCF cycle has converged
        absolute : bool, default=True
            whether to plot the absolute value of the energies
        title : str | None, default=None
            system name to include in title

        Returns
        -------
        axes.Axes
            matplotlib subplot object
        """
        if absolute:
            delta_sum_eigenvalues = np.abs(delta_sum_eigenvalues)
            delta_total_energies = np.abs(delta_total_energies)

        ax.plot(
            tot_scf_iters,
            delta_sum_eigenvalues,
            label=r"$\Delta \; \Sigma$ eigenvalues",
            c="C1",
        )
        ax.plot(
            tot_scf_iters,
            delta_total_energies,
            label=r"$\Delta$ total energies",
            c="C0",
        )

        # Add the convergence parameters
        if conv_params is not None:
            ax.axhline(
                conv_params["sum_eigenvalues"],
                ls="-.",
                c="darkgray",
                label=r"$\Delta \; \Sigma$ eigenvalues convergence criterion",
            )
            ax.axhline(
                conv_params["total_energy"],
                ls="--",
                c="gray",
                label=r"$\Delta$ total energies convergence criterion",
            )

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_yscale("log")
        ax.set_xlabel("cumulative SCF iteration")
        ax.set_ylabel(r"absolute energy / $| \mathrm{eV} |$")
        ax.legend()
        if title is not None:
            ax.set_title(rf"{title} Energies and Eigenvalues Convergence")

        return ax

    @staticmethod
    def _plot_forces_convergence(
        ax: axes.Axes,
        forces_on_atoms: npt.NDArray[np.float64] | list[float],
        conv_params: dict | None = None,
        title: str | None = None,
    ) -> None:
        """
        Create a subplot for the forces convergence of an FHI-aims calculation.

        Parameters
        ----------
        ax : axes.Axes
            matplotlib subplot index
        forces_on_atoms : npt.NDArray[np.float64] | list[float]
            all forces acting on each atom
        conv_params : dict | None, default=None
            convergence parameters which determine if the SCF cycle has converged
        title : str | None, default=None
            system name to include in title
        """
        # see NOTE in dfttoolkit.output.AimsOutput.get_i_scf_conv_acc()
        # ax.plot(delta_forces, label=r"$\Delta$ forces")  # noqa: ERA001
        ax.plot(forces_on_atoms, label="forces on atoms")

        # Add the convergence parameters
        if conv_params is not None and conv_params["total_force"] is not None:
            ax.axhline(
                conv_params["total_force"],
                ls="--",
                c="gray",
                label="forces convergence criterion",
            )

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("geometry relaxation step")
        ax.set_ylabel(r"force / $\mathrm{eV} \mathrm{\AA}^{-1}$")
        ax.legend()

        if title is not None:
            ax.set_title(rf"{title} Forces Convergence")

    @staticmethod
    def _plot_ks_states_convergence(
        ax: axes.Axes,
        ks_eigenvals: dict[str, npt.NDArray[np.int64 | np.float64]]
        | tuple[
            dict[str, npt.NDArray[np.int64 | np.float64]],
            dict[str, npt.NDArray[np.int64 | np.float64]],
        ],
        title: str | None = None,
    ) -> None:
        """
        Create a subplot for the energy changes of the KS eigenstates.

        Parameters
        ----------
        ax : axes.Axes
            matplotlib subplot index
        ks_eigenvals : dict | tuple[npt.NDArray, npt.NDArray]
            state, occupation, and eigenvalue of each KS state at each SCF
            iteration
        title : str | None, default=None
            system name to include in title

        Returns
        -------
        axes.Axes
            matplotlib subplot object
        """
        if isinstance(ks_eigenvals, dict):
            # Don't include last eigenvalue as it only prints after final SCF iteration
            # Add 1 to total SCF iterations to match the length of the eigenvalues and
            # we want to include the first pre SCF iteration
            for ev in ks_eigenvals["eigenvalue_eV"].T:
                ax.plot(np.arange(len(ks_eigenvals["eigenvalue_eV"])), ev)

        elif isinstance(ks_eigenvals, tuple):
            su_ks_eigenvals = ks_eigenvals[0]
            sd_ks_eigenvals = ks_eigenvals[1]

            for ev in su_ks_eigenvals["eigenvalue_eV"].T:
                ax.plot(np.arange(len(su_ks_eigenvals["eigenvalue_eV"])), ev, c="C0")

            for ev in sd_ks_eigenvals["eigenvalue_eV"].T:
                ax.plot(np.arange(len(su_ks_eigenvals["eigenvalue_eV"])), ev, c="C1")

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_yscale("symlog")
        ax.set_xlabel("cumulative SCF iteration")
        ax.set_ylabel("energy / eV")

        if title is not None:
            ax.set_title(f"{title} KS State Convergence")

    def convergence(
        self,
        conv_params: dict | None = None,
        scf_conv_acc_params: dict | None = None,
        title: str | None = None,
        forces: bool = False,
        ks_eigenvalues: bool = False,
        fig_size: tuple[int, int] = (24, 6),
    ) -> figure.Figure:
        """
        Plot the SCF convergence accuracy parameters.

        Parameters
        ----------
        conv_params: dict | None, default=None
            convergence parameters which determine if the SCF cycle has converged
        scf_conv_acc_params : dict | None, default=None
            the scf convergence accuracy parameters
        title : str | None, default=None
            system name to use in title of the plot
        forces : bool, default=False
            whether to plot the change of forces and forces on atoms
        ks_eigenvalues : bool, default=False
            whether to plot the kohn-sham eigenvalues
        fig_size : tuple[int, int], default=(24, 6)
            the total size of the figure

        Returns
        -------
        figure.Figure
            matplotlib figure object
        """
        # Get the SCF convergence accuracy parameters if not provided
        if scf_conv_acc_params is None:
            if not hasattr(self, "scf_conv_acc_params"):
                self.scf_conv_acc_params = self.get_i_scf_conv_acc()

        # Override the default scf_conv_acc_params if given in function
        else:
            self.scf_conv_acc_params = scf_conv_acc_params

        scf_iters = self.scf_conv_acc_params["scf_iter"]
        tot_scf_iters = np.arange(1, len(scf_iters) + 1)
        delta_charge = self.scf_conv_acc_params["change_of_charge"]
        delta_charge_sd = self.scf_conv_acc_params["change_of_charge_spin_density"]
        delta_sum_eigenvalues = self.scf_conv_acc_params["change_of_sum_eigenvalues"]
        delta_total_energies = self.scf_conv_acc_params["change_of_total_energy"]

        # Change the number of subplots if forces and ks_eigenvalues are to be plotted
        subplots = [True, True, forces, ks_eigenvalues]
        i_subplot = 1

        # Setup the figure subplots
        fig, ax = plt.subplots(1, subplots.count(True), figsize=fig_size)

        # Plot the change of charge
        self._plot_charge_convergence(
            ax[0], tot_scf_iters, delta_charge, delta_charge_sd, conv_params, title
        )

        # Plot the change of total energies and sum of eigenvalues
        self._plot_energy_convergence(
            ax[1],
            tot_scf_iters,
            delta_sum_eigenvalues,
            delta_total_energies,
            conv_params,
            True,
            title,
        )

        # Plot the forces
        if forces:
            # see NOTE in dfttoolkit.output.AimsOutput.get_i_scf_conv_acc()
            # delta_forces = self.scf_conv_acc_params["change_of_forces"]  # noqa: E501, ERA001
            # delta_forces = np.delete(delta_forces, np.argwhere(delta_forces == 0.0))  # noqa: E501, ERA001
            forces_on_atoms = self.scf_conv_acc_params["forces_on_atoms"]
            forces_on_atoms = np.delete(
                forces_on_atoms, np.argwhere(forces_on_atoms == 0.0)
            )
            i_subplot += 1
            self._plot_forces_convergence(
                ax[i_subplot], forces_on_atoms, conv_params, title
            )

        # Plot the KS state energies
        if ks_eigenvalues:
            i_subplot += 1
            ks_eigenvals = self.get_all_ks_eigenvalues()

            self._plot_ks_states_convergence(ax[i_subplot], ks_eigenvals, title)

        return fig


class VisualiseCube(Cube):
    """
    Cube visualisation tools.

    ...

    Attributes
    ----------
    path : str
        path to the .cube file
    lines : list[str]
        contents of the .cube file
    atoms : Atom | Atoms
        ASE atom or atoms object
    volume : NDArray[float64]
        volumetric data of the cube file

    Parameters
    ----------
    cube : str
        path to the .cube file
    """

    def __init__(self, cube: str):
        super().__init__(cube=cube)

    def weas_core_hole(
        self, viewer: WeasWidget | None = None, **kwargs: str
    ) -> WeasWidget:
        """
        Visualise the core hole as an isosurface.

        Parameters
        ----------
        viewer : WeasWidget | None, default=None
            viewer instance
        **kwargs
            viewer settings keyword arguments

        Returns
        -------
        WeasWidget
            viewer instance
        """
        # Check if running in Jupyter
        try:
            from IPython import get_ipython  # pyright: ignore

            if (
                not mo.running_in_notebook()
                or get_ipython().__class__.__name__ != "ZMQInteractiveShell"
            ):
                raise NotImplementedError(
                    "The core_hole method is only available in a Jupyter session."
                )

        except (ImportError, AttributeError):
            return False

        # Create the viewer
        ch_viewer = WeasWidget(**kwargs) if viewer is None else viewer

        ch_viewer.from_ase(self.atoms)
        ch_viewer.avr.model_style = 1  # Ball and stick
        ch_viewer.avr.iso.volumetric_data = {"values": self.volume}
        ch_viewer.avr.iso.settings = {
            "positive": {"isovalue": -0.03, "color": "red"},
            "negative": {"isovalue": 0.03, "color": "blue"},
        }

        return ch_viewer
