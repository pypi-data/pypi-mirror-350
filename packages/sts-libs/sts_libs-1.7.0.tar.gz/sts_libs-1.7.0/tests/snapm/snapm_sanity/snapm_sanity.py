#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


from os import getenv
from typing import TYPE_CHECKING

import pytest

from sts.lvm import LogicalVolume
from sts.snapm.snapset import Snapset
from sts.utils.files import count_files

if TYPE_CHECKING:
    from sts.utils.files import Directory


@pytest.mark.usefixtures('_snapm_test')
class TestSnapm:
    @pytest.mark.parametrize(
        'fixture_name',
        [
            pytest.param('mount_lv', id='lvm2-cow'),
            pytest.param('mount_thin_lv', id='lvm2-thin'),
        ],
    )
    def test_lvm2_snapshots(self, request: pytest.FixtureRequest, fixture_name: str) -> None:
        """Test basic snapset operations with LVM.

        Tests the creation, listing, renaming, and deletion of snapsets
        on mounted LVM volumes.

        Args:
            request: pytest request fixture
            fixture_name: name of the fixture providing a mounted LV
        """
        snapset_name = getenv('STS_SNAPSET_NAME', 'stssnapset1')
        snapset_rename = getenv('STS_SNAPSET_RENAME', 'stssnapsetrename')
        mount_point: Directory = request.getfixturevalue(fixture_name)
        n_files = count_files(mount_point.path)
        flag = mount_point.path / 'FLAG'
        flag.write_text('SNAPMTEST')

        assert flag.exists

        # Create snapset using the new Snapset class
        snapset = Snapset()
        assert snapset.create(snapset_name=snapset_name, size_policy='80%FREE', sources=[str(mount_point.path)]), (
            f'Failed to create snapset {snapset_name}'
        )

        # Verify that LVM snapshot was created
        lv = LogicalVolume()
        lv_result = lv.lvs()
        assert lv_result.succeeded
        assert f'snapset_{snapset_name}' in lv_result.stdout

        assert snapset.rename(snapset_rename), f'Failed to rename snapset from {snapset_name} to {snapset_rename}'
        if snapset.info:
            assert snapset.info.name == snapset_rename

        assert count_files(mount_point.path) == n_files + 1
        mount_point.remove_file(flag)
        assert count_files(mount_point.path) == n_files

        # Activate/Deactivate doesn't have effect on COW snapshots
        if 'thin' in fixture_name and snapset.info:
            assert snapset.activate()
            assert snapset.info.status == 'Active'

            assert snapset.deactivate()
            assert snapset.info.status == 'Inactive'

            assert snapset.autoactivate(enable=True)
            assert snapset.info.autoactivate is True

            assert snapset.autoactivate(enable=False)
            assert snapset.info.autoactivate is False

        assert snapset.delete(), f'Failed to delete snapset {snapset_rename}'

        lv_result = lv.lvs()
        assert f'snapset_{snapset_rename}' not in lv_result.stdout
