from magma_var.resources import event_codes, colors, columns
from magma_var.utils import check_directory
from typing import Tuple
from datetime import datetime, timedelta
from pandas.errors import EmptyDataError
from pathlib import Path
import os
import json
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def validate_earthquake_events(earthquake_events: str | list[str] = None) -> list[str]:
    if earthquake_events is None:
        return ['*']

    if isinstance(earthquake_events, str):
        earthquake_events = [earthquake_events]

    for earthquake_event in earthquake_events:
        if earthquake_event not in event_codes:
            raise ValueError("Earthquake_events must be one of '*', 'lts', 'apl', 'apg', 'gug', 'hbs', 'hrm', "
                             "'tre', 'tor', 'lof', 'hyb', 'vtb', 'vta','vlp', 'tel', 'trs', 'tej', 'dev', 'gtb', "
                             "'dpt', 'mtr'")

    return earthquake_events


class Plot:
    url_evaluasi = 'https://magma.esdm.go.id/api/v1/python/magma-var/evaluasi'

    def __init__(self, token: str, volcano_code: str = None, start_date: str = None, end_date: str = None,
                 earthquake_events: str | list[str] = None, current_dir: str = None, verbose: bool = False) -> None:

        self.token = token
        self.volcano_code = volcano_code
        self.start_date = start_date
        self.end_date = end_date
        self.earthquake_events: list[str] = validate_earthquake_events(earthquake_events)
        self.verbose = verbose
        self.figsize = (12,1)
        self.figure_ylabel_x = 0.07
        self.figure_ylabel_fontsize = 12
        self.title_y_location = 0.92
        self.title_fontszie = 12
        self.legend_fontsize = 8
        self.x_labelsize = 8
        self.y_labelsize = 8

        self.json: dict = self.get_json_response()
        self.df: pd.DataFrame = self.get_df()
        self.events_not_recorded = self.df.columns[self.df.sum() == 0]
        self.filename = 'magma_{}_{}_{}'.format(self.volcano_code, self.start_date, self.end_date)

        if current_dir is None:
            current_dir = os.getcwd()
        self.current_dir = current_dir

        self.output_dir, self.figures_dir, self.magma_dir = check_directory(current_dir)

        if start_date is None:
            self.start_date: str = datetime.today().strftime('%Y-%m-%d')

        if end_date is None:
            self.end_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')

        self.csv = self.download()

    def get_df(self, json_response: dict = None) -> pd.DataFrame:
        if json_response is None:
            json_response = self.json

        df = pd.json_normalize(json_response['data'])
        df.drop(columns=[
            'availability',
            'visual.visibility',
            'visual.cuaca',
            'visual.asap.teramati',
            'visual.asap.warna',
            'visual.asap.intensitas',
            'visual.asap.tekanan',
            'visual.asap.tinggi_min',
            'visual.asap.tinggi_max',
            'visual.letusan.teramati',
            'visual.letusan.tinggi_min',
            'visual.letusan.tinggi_max',
            'visual.letusan.warna',
            'visual.awan_panas_guguran.teramati',
            'visual.awan_panas_guguran.jarak_min',
            'visual.awan_panas_guguran.jarak_max'
        ], inplace=True)

        df.drop(columns=df.columns[df.sum() == 0], inplace=True)
        df.set_index(keys='date', inplace=True)
        df.index = pd.to_datetime(df.index)

        df.rename(columns=columns, inplace=True)

        if 'Tremor Menerus' in df.columns:
            df.drop(columns=['Tremor Menerus'], inplace=True)

        return df

    def get_json_response(self, token: str = None) -> dict:

        if token is None:
            token = self.token

        url = self.url_evaluasi

        payload = json.dumps({
            "start_date": self.start_date,
            "end_date": self.end_date,
            "code_ga": self.volcano_code,
            "gempa": self.earthquake_events
        })

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        start_date_object = datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date_object = datetime.strptime(self.end_date, "%Y-%m-%d")

        if start_date_object > end_date_object:
            raise ValueError(
                'End date ({}) must be greater than start date ({})'.format(self.end_date, self.start_date))

        if (end_date_object > datetime.now()) or (start_date_object > datetime.now()):
            raise ValueError('End date or start date must not greater than today ({})'.format(datetime.today().date()))

        try:
            response = requests.request("GET", url, headers=headers, data=payload).json()
        except Exception as e:
            raise ValueError(f'Please check your token or parameters {payload}. Error: {e}')

        if 'code' in response:
            if response['code'] == 401:
                raise ValueError(f'Please update your token at https://magma.esdm.go.id/chambers/token')

        if 'errors' in response:
            raise ValueError(response['errors'])

        if self.verbose:
            print(response)

        return response

    def download(self) -> str:
        """Download daily seismic from MAGMA Indonesia

        Returns:
            str: path to downloaded file
        """
        if not self.df.empty:
            try:
                csv = os.path.join(self.magma_dir, "{}.csv".format(self.filename))
                self.df.to_csv(csv)
                self.csv = csv
                print(f'💾 Saved to {csv}')

                return csv
            except Exception as e:
                raise FileNotFoundError(f'Failed to save csv file: {e}')
        else:
            print('⚠️ There is no event(s) between {} and {}. '
                  'Please change your parameters.'.format(self.start_date, self.end_date))
            raise EmptyDataError

    def from_csv(self, csv: str, interval: int = 1, width: float = 0.5, save_plot: bool = True,
                 title: str = None, dpi: int = 300) -> Tuple[plt.Figure, plt.Axes]:
        """Plot from csv file.

        Args:
            csv (str): path to csv file
            interval (int, optional): Xtick label interval (day). Defaults to 1.
            width (float, optional): Width of column bar. Defaults to 0.5.
            save_plot (bool, optional): Save plot. Defaults to True.
            title (str, optional): Title of plot. Defaults to 'Kegempaan'.
            dpi (int, optional): Image resolution. Defaults to 300.

        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure, Axes
        """

        if title is None:
            title = 'Kegempaan'

        figure_width, figure_height = self.figsize

        filename = Path(csv).stem

        df = pd.read_csv(csv, index_col='date', parse_dates=True)

        fig, axs = plt.subplots(
            nrows=len(df.columns),
            ncols=1,
            figsize=(figure_width, figure_height * len(df.columns)),
            sharex=True
        )

        plt.subplots_adjust(hspace=0.0)

        for gempa, column_name in enumerate(df.columns):
            Plot.ax(
                ax=axs[gempa],
                df=df,
                column_name=column_name,
                width=width,
                interval=interval,
                legend_fontsize=self.legend_fontsize,
                x_labelsize=self.x_labelsize,
                y_labelsize=self.y_labelsize
            )

        fig.supylabel('Jumlah', x=self.figure_ylabel_x, fontsize=self.figure_ylabel_fontsize)
        fig.suptitle(title, fontsize=self.title_fontszie, y=self.title_y_location)

        if save_plot:
            figure_name = os.path.join(self.figures_dir, f'{filename}.png')
            print(f'📷 Saved to : {figure_name}')
            fig.savefig(figure_name, dpi=dpi)

        return fig, axs

    def show(self, interval: int = 1, width: float = 0.5, save_plot: bool = True,
             title: str = None, dpi: int = 300, figsize: Tuple[int, int] = (12, 1),
             title_y_location: float = 0.92, title_fontsize: int = 12,
             figure_ylabel_x: float = 0.07, figure_ylabel_fontsize: int = 12,
             legend_fontsize: int = 8, x_labelsize: int = 8, y_labelsize: int = 8) -> Tuple[plt.Figure, plt.Axes]:
        """Show plot in matplotlib

        Args:
            interval (int, optional): Xtick label interval (day). Defaults to 1.
            width (float, optional): Width of column bar. Defaults to 0.5.
            save_plot (bool, optional): Save plot. Defaults to True.
            title (str, optional): Title of plot. Defaults to 'Kegempaan'.
            dpi (int, optional): Image resolution. Defaults to 300.
            figsize (tuple(int, int), optional): Size of figure. Defaults to (12, 1).
            title_y_location (float, optional): Location of title. Defaults to 0.92.
            title_fontsize (int, optional): Font size of title. Defaults to 12.
            figure_ylabel_x (float, optional): Location x of figure. Defaults to 0.07.
            figure_ylabel_fontsize (int, optional): Font size of figure. Defaults to 12.
            legend_fontsize (int, optional): Font size of legend. Defaults to 8.
            x_labelsize (int, optional): Font size of x-axis label. Defaults to 8.
            y_labelsize (int, optional): Font size of y-axis label. Defaults to 8.

        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure, Axes
        """
        self.figsize = figsize
        self.title_y_location = title_y_location
        self.title_fontszie = title_fontsize
        self.figure_ylabel_fontsize = figure_ylabel_fontsize
        self.figure_ylabel_x = figure_ylabel_x
        self.legend_fontsize = legend_fontsize

        self.x_labelsize = x_labelsize
        self.y_labelsize = y_labelsize

        return self.from_csv(
            csv=self.csv,
            interval=interval,
            width=width,
            save_plot=save_plot,
            title=title,
            dpi=dpi
        )

    @staticmethod
    def ax(ax: plt.Axes, df: pd.DataFrame, column_name: str, width: float = 0.5, interval=1,
           legend_fontsize = 8, x_labelsize = 8, y_labelsize = 8) -> plt.Axes:

        ax.bar(df.index, df[column_name], width=width, label=column_name,
               color=colors[column_name], linewidth=0)

        ax.legend(loc=2, fontsize=legend_fontsize)

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax.yaxis.get_major_ticks()[0].label1.set_visible(False)
        ax.set_xlim(df.first_valid_index(), df.last_valid_index())

        ax.set_ylim([0, df[column_name].max() * 1.2])

        for label in ax.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

        ax.tick_params(axis='y', labelsize=x_labelsize)
        ax.tick_params(axis='x', labelsize=y_labelsize)

        # for key, continuous in enumerate(continuous_eruptions):
        #     # continuous[0] = start date of eruption
        #     # continuous[1] = end date of eruption
        #     axs[gempa].axvspan(continuous[0], continuous[1], alpha=0.4,
        #                        color='orange', label="_" * key + 'Continuous Eruption')
        #
        # for key, date in enumerate(single_eruptions):
        #     axs[gempa].axvline(datetime.strptime(date, '%Y-%m-%d'),
        #                        color='red', label="_" * key + 'Single Eruption')

        return ax
