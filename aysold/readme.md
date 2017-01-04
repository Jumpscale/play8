- switch branch

```bash
cd /opt/code/github/jumpscale/jumpscale_core7
git fetch oriring ays_unstable:ays_unstable
git checkout ays_unstable

cd /opt/code/github/jumpscale/ays_jumpscale7
git fetch oriring ays_unstable:ays_unstable
git checkout ays_unstable
```

- link last added lib

```bash
ln -s /opt/code/git/binary/base_python/root/lib/pytoml/ /opt/jumpscale7/lib
```

- load ssh-agent

```
eval `ssh-agent -s`
```