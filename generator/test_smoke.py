import tsv2json
import generator


def test_all(tmpdir):
    tsv2json.run('demodata.tsv', 'demomatches.tsv', str(tmpdir))
    generator.run(str(tmpdir.join('demodata.json')), str(tmpdir.join('demomatches.json')),
                  str(tmpdir))
    assert tmpdir.join('index.html').check(file=1)
    assert tmpdir.join('matchinfo.csv').check(file=1)
