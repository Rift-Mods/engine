// namespace Patcher;
using System.Reflection;
using HarmonyLib;
public class Patcher
{
    public static void Patch(string path)
    {
        // return path;
        var dll = Assembly.LoadFile(path);
        var harmony = new Harmony("riftmodding.patches");
        harmony.PatchAll(dll);
    }
}
